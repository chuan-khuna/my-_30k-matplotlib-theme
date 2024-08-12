import pandas as pd
import numpy as np
import datetime
from typing import Callable


def select_labels(labels: list, num: int, label_type: str) -> list:
    """Select lowest `num` elements from a list of labels"""

    if label_type == 'asc':
        return labels[:num]
    else:
        return labels[-num:]


def safe_qcut(
    data: pd.Series | np.ndarray | list, q: int, label_type: str = 'asc', unique=False
) -> tuple[pd.Series, dict]:

    assert label_type in ['asc', 'desc'], "`label_type` must be either 'asc' or 'desc'"

    data_series = pd.Series(data)

    if unique:
        # generate quantile criteria based on unique values
        qcut_data = data_series.unique()
    else:
        qcut_data = np.array(data_series)

    # get the actual number of bins
    num_bins = len(pd.qcut(qcut_data, q, duplicates='drop').categories)

    # while all elements are the same
    if num_bins == 0:
        raise ValueError(
            f"The number of bins is {num_bins} because num unique values = {data_series.nunique()}"
        )

    qcut_intervals = pd.qcut(qcut_data, num_bins, duplicates='drop')

    result = pd.Categorical(data_series, categories=qcut_intervals.categories, ordered=True)

    # return quantile criteria
    interval_dict = {}
    for i, interval in enumerate(qcut_intervals.categories):

        if label_type == 'asc':
            code = i + 1
        else:
            code = i + 1
            # reverse the code
            code = abs(code - (num_bins + 1))

        interval_dict[str(interval)] = code

    return pd.Series(result), interval_dict


def compute_recency(
    df, id_col: str, date_col: str, recent_date: datetime.datetime | None
) -> pd.Series:
    # automatically detect the most recent date from the dataset
    if recent_date is None:
        recent_date = df[date_col].max()

    recent_date_df = df.groupby(id_col)[date_col].max().reset_index()

    recent_date_df['r'] = (recent_date - recent_date_df[date_col]).dt.days

    return recent_date_df[[id_col, 'r']]


def compute_frequency(df, id_col: str, date_col: str) -> pd.Series:
    # count frequency of each unique customer, by sale date
    frequency_df = df.groupby(id_col).agg({date_col: 'count'}).reset_index()
    frequency_df = frequency_df.rename(columns={date_col: 'f'})

    return frequency_df


def compute_monetary(df, id_col: str, monetary_col: str) -> pd.Series:
    # sum the total retail price of each unique customer
    monetary_df = df.groupby(id_col).agg({monetary_col: 'sum'}).reset_index()
    monetary_df = monetary_df.rename(columns={monetary_col: 'm'})

    return monetary_df


def process_rfm(
    df: pd.DataFrame,
    in_customer_col: str,
    in_monetary_col: str,
    in_date_col: str,
    recency_last_date: datetime.datetime | None = None,
    out_customer_col: str = 'customer_id',
    out_recency_col: str = 'recency',
    out_frequency_col: str = 'frequency',
    out_monetary_col: str = 'monetary',
) -> pd.DataFrame:

    r_df = compute_recency(df, in_customer_col, in_date_col, recency_last_date)
    f_df = compute_frequency(df, in_customer_col, in_date_col)
    m_df = compute_monetary(df, in_customer_col, in_monetary_col)

    result = pd.concat(
        [
            r_df.set_index(in_customer_col),
            f_df.set_index(in_customer_col),
            m_df.set_index(in_customer_col),
        ],
        axis=1,
    ).reset_index()

    result = result.rename(
        columns={
            in_customer_col: out_customer_col,
            'r': out_recency_col,
            'f': out_frequency_col,
            'm': out_monetary_col,
        }
    )

    return result


def process_rfm_with_score(
    df: pd.DataFrame,
    in_customer_col: str,
    in_monetary_col: str,
    in_date_col: str,
    r_score_func: Callable[[pd.Series[int | float]], tuple[pd.Series[int], dict[str, int]]],
    f_score_func: Callable[[pd.Series[int | float]], tuple[pd.Series[int], dict[str, int]]],
    m_score_func: Callable[[pd.Series[int | float]], tuple[pd.Series[int], dict[str, int]]],
    recency_last_date: datetime.datetime | None = None,
    out_customer_col: str = 'customer_id',
    out_recency_col: str = 'recency',
    out_frequency_col: str = 'frequency',
    out_monetary_col: str = 'monetary',
) -> tuple[pd.DataFrame, dict]:

    result = process_rfm(
        df,
        in_customer_col,
        in_monetary_col,
        in_date_col,
        recency_last_date,
        out_customer_col,
        out_recency_col,
        out_frequency_col,
        out_monetary_col,
    )

    result[out_recency_col + '_score'], recency_criteria = r_score_func(result[out_recency_col])
    result[out_frequency_col + '_score'], frequency_criteria = f_score_func(
        result[out_frequency_col]
    )
    result[out_monetary_col + '_score'], monetary_criteria = m_score_func(result[out_monetary_col])

    result['rfm_score'] = (
        result[out_recency_col + '_score'].astype(str)
        + result[out_frequency_col + '_score'].astype(str)
        + result[out_monetary_col + '_score'].astype(str)
    )

    criteria = {
        'recency': recency_criteria,
        'frequency': frequency_criteria,
        'monetary': monetary_criteria,
    }

    return result, criteria


def process_score(series, q, label_type, unique=True):
    res, criteria = safe_qcut(series, q, label_type, unique=unique)
    return res.apply(lambda x: criteria[str(x)]), criteria
