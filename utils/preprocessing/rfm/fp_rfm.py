import pandas as pd
import numpy as np
import datetime


def safe_qcut(
    data: pd.Series | np.ndarray | list, q: int, labels: list, label_type: str = 'asc'
) -> tuple[pd.Series, dict]:

    assert label_type in ['asc', 'desc'], "`label_type` must be either 'asc' or 'desc'"
    assert (
        len(labels) >= q
    ), "The number of labels must be greater than or equal to the number of bins"

    if label_type == 'asc':
        assert labels == sorted(
            labels
        ), f"Labels must be in ascending order: {labels =}, {label_type =}"
    else:
        assert labels == sorted(
            labels, reverse=True
        ), f"Labels must be in descending order: {labels =}, {label_type =}"

    data_series = pd.Series(data)

    # get the actual number of bins
    num_bins = len(pd.qcut(data_series, q, duplicates='drop').cat.categories)

    # while all elements are the same
    if num_bins == 0:
        raise ValueError(
            f"The number of bins is {num_bins} because num unique values = {data_series.nunique()}"
        )

    # when number of bins is not equal to the number of labels
    # assign label from the lowest to the highest
    if num_bins != len(labels):
        if label_type == 'asc':
            # higher value = better label
            selected_labels = labels[:num_bins]
        else:
            # higher value = worse label
            selected_labels = labels[-num_bins:]
    else:
        selected_labels = labels

    qcut_labels = pd.qcut(data_series, q, duplicates='drop', labels=selected_labels)
    qcut_intervals = pd.qcut(data_series, q, duplicates='drop')

    # return quantile criteria
    interval_dict = {}
    for i, interval in enumerate(qcut_intervals.cat.categories):
        interval_dict[f"({interval.left}, {interval.right}]"] = selected_labels[i]

    return qcut_labels, interval_dict


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
    # count frequency of each unique customer, by order date
    frequency_df = df.groupby(id_col).agg({date_col: 'count'}).reset_index()
    frequency_df = frequency_df.rename(columns={date_col: 'f'})

    return frequency_df


def compute_monetary(df, id_col: str, monetary_col: str) -> pd.Series:
    # sum the order total of each unique customer
    monetary_df = df.groupby(id_col).agg({monetary_col: 'sum'}).reset_index()
    monetary_df = monetary_df.rename(columns={monetary_col: 'm'})

    return monetary_df


def process_rfm(
    df: pd.DataFrame,
    in_customer_col: str,
    in_monetary_col: str,
    in_date_col: str,
    recency_last_date: datetime.datetime | None = None,
    n_quantiles: int = 5,
    out_customer_col: str = 'customer_id',
    out_recency_col: str = 'recency',
    out_frequency_col: str = 'frequency',
    out_monetary_col: str = 'monetary',
) -> tuple[pd.DataFrame, dict]:
    asc_labels = list(range(1, n_quantiles + 1))
    desc_labels = list(range(n_quantiles, 0, -1))

    r = compute_recency(df, in_customer_col, in_date_col, recency_last_date)
    f = compute_frequency(df, in_customer_col, in_date_col)
    m = compute_monetary(df, in_customer_col, in_monetary_col)

    result = pd.concat(
        [r.set_index(in_customer_col), f.set_index(in_customer_col), m.set_index(in_customer_col)],
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

    result[out_recency_col + '_score'], recency_intervals = safe_qcut(
        result[out_recency_col], n_quantiles, desc_labels, 'desc'
    )
    result[out_frequency_col + '_score'], frequency_intervals = safe_qcut(
        result[out_frequency_col], n_quantiles, asc_labels
    )
    result[out_monetary_col + '_score'], monetary_intervals = safe_qcut(
        result[out_monetary_col], n_quantiles, asc_labels
    )

    crirtetia = {
        'recency': recency_intervals,
        'frequency': frequency_intervals,
        'monetary': monetary_intervals,
    }

    return result, crirtetia
