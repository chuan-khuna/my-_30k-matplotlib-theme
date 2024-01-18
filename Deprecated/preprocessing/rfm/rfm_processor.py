import pandas as pd
import numpy as np


class RFMProcessor:

    def __init__(self,
                 customer: str,
                 date: str,
                 monetary: str,
                 recency_last_date: str = None,
                 n_groups: int = 5,
                 id_col: str = 'customer',
                 R_col: str = 'recency',
                 F_col: str = 'frequency',
                 M_col: str = 'monetary'):
        """
        An input dataframe for this function should be grouped by `order id`. 
        Each "order" should have ONLY 1 row.

        Args:
            customer (str): an input dataframe's column to distinguise customers
            date (str): an input dataframe's date column
            monetary (str): an input dataframe's monetary column, ie `total`
            recency_last_date (str, optional): last date to calculate `R_value` in format `YYYY-MM-DD`. Defaults to None.
            n_groups (int, optional): the number of groups for `pd.qcut`
            id_col (str, optional): output column for `customer_id`. Defaults to 'customer'.
            R_col (str, optional): output column for `R_value`. Defaults to 'recency'.
            F_col (str, optional): output column for `F_value`. Defaults to 'frequency'.
            M_col (str, optional): output column for `M_value`. Defaults to 'monetary'.
        """

        self.customer_col = customer
        self.date_col = date
        self.monetary_col = monetary

        self.recency_last_date = recency_last_date

        self.id_col = id_col
        self.R_col = R_col
        self.F_col = F_col
        self.M_col = M_col

        self.n_groups = n_groups

    def __reset_index_rename(self, df: pd.DataFrame, columns_dict: dict[str, str]) -> pd.DataFrame:
        df = df.reset_index()
        df = df.rename(columns=columns_dict)
        return df

    def _compute_monetary_value(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.groupby(self.customer_col).agg({self.monetary_col: 'sum'})
        result = self.__reset_index_rename(result, {
            self.customer_col: self.id_col,
            self.monetary_col: self.M_col
        })
        return result

    def _compute_frequency_value(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.date_col] = pd.to_datetime(df[self.date_col])
        result = df.groupby(self.customer_col).agg({self.date_col: 'count'})
        result = self.__reset_index_rename(result, {
            self.customer_col: self.id_col,
            self.date_col: self.F_col
        })
        return result

    def _compute_recency_value(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.date_col] = pd.to_datetime(df[self.date_col])

        if self.recency_last_date:
            last_date = pd.to_datetime(self.recency_last_date)
        else:
            last_date = df[self.date_col].max()

        result = df.groupby(self.customer_col).agg({self.date_col: 'max'})

        result = self.__reset_index_rename(result, {
            self.customer_col: self.id_col,
            self.date_col: self.R_col
        })

        result[self.R_col] = (last_date - result[self.R_col]).dt.days

        return result

    def __safe_qcut(self, x: pd.Series, labels: list) -> pd.Series:
        """A pandas's `qcut` wrapper to safely compute

        Args:
            x (pd.Series): _description_
            labels (list): _description_

        Returns:
            pd.Series: _description_
        """

        # if any errors occur set default to the best score
        # it depends on whether `labels` is reversed or not
        # ie lower value = higher score
        try:
            n_bins = len(pd.qcut(x, self.n_groups, duplicates='drop').cat.categories)

            if labels[0] > labels[1]:
                return pd.qcut(x, self.n_groups, labels[:n_bins], duplicates='drop')
            else:
                return pd.qcut(x, self.n_groups, labels[-n_bins:], duplicates='drop')

        except Exception as e:
            return pd.Series(np.ones_like(x) * self.n_groups).astype(int)

    def process_value(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process input dataframe, eg POS history
        return a dataframe of "RFM values"

        Args:
            df (pd.DataFrame): _description_

        Returns:
            pd.DataFrame: _description_
        """

        R = self._compute_recency_value(df)
        F = self._compute_frequency_value(df)
        M = self._compute_monetary_value(df)

        RFM = pd.concat(
            [R.set_index(self.id_col),
             F.set_index(self.id_col),
             M.set_index(self.id_col)], axis=1)
        RFM = RFM.reset_index()
        return RFM

    def process_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process input dataframe, eg POS history
        return a dataframe of RFM values and RFM score.

        Args:
            df (pd.DataFrame): _description_

        Returns:
            pd.DataFrame: _description_
        """
        RFM = self.process_value(df)

        labels = list(range(1, self.n_groups + 1))

        RFM[self.R_col + '_score'] = self.__safe_qcut(RFM[self.R_col], labels=labels[::-1])
        RFM[self.F_col + '_score'] = self.__safe_qcut(RFM[self.F_col], labels=labels)
        RFM[self.M_col + '_score'] = self.__safe_qcut(RFM[self.M_col], labels=labels)

        RFM['rfm_score'] = RFM[[
            self.R_col + '_score', self.F_col + '_score', self.M_col + '_score'
        ]].apply(lambda row: f"{row[0]}{row[1]}{row[2]}", axis=1)
        return RFM
