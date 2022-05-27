# CSV Line and Word Info Counts
from dataclasses import dataclass
from functools import lru_cache

import pandas as pd
import numpy as np


@dataclass
class InfoDF:
    df: pd.DataFrame

    @lru_cache(maxsize=None)
    def str_column(self, column: str) -> pd.Series:
        """
        Gets a pd series of the specified column, cast to str and dropped NaNs
        :param column: Name of column
        :return: pd series of the specified column
        """
        return self.df[column].astype(str).dropna()

    @lru_cache(maxsize=None)
    def stat_lengths(self, column: str) -> np.array:
        """
        Gets a list of str lengths in specified column
        :param column: Name of column
        :return: numpy array of str lengths
        """
        # Get a list of str lengths
        return np.array(self.str_column(column).str.len())

    @lru_cache(maxsize=None)
    def stat_freq_words(self, column: str) -> pd.DataFrame:
        """
        Returns a dataframe of word and frequencies
        :param column: Name of column
        :return: Dataframe of word and frequencies
        """
        return self.str_column(column).str.split(expand=True).stack().value_counts()


def count()
