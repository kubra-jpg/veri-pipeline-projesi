# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_cleaner import clean_dates, fill_missing_postal_codes, add_derived_columns, detect_outliers_iqr


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Order Date':  ['01/01/2021', '15/06/2022', '30/12/2023'],
        'Ship Date':   ['05/01/2021', '20/06/2022', '03/01/2024'],
        'Postal Code': [10001.0, None, 90210.0],
        'Sales':       [100.0, 5000.0, 250.0],
    })


def test_clean_dates(sample_df):
    df = clean_dates(sample_df)
    assert pd.api.types.is_datetime64_any_dtype(df['Order Date'])
    assert pd.api.types.is_datetime64_any_dtype(df['Ship Date'])


def test_fill_missing_postal_codes(sample_df):
    df = fill_missing_postal_codes(sample_df)
    assert df['Postal Code'].isnull().sum() == 0
    assert df['Postal Code'].dtype == int


def test_add_derived_columns(sample_df):
    df = clean_dates(sample_df)
    df = add_derived_columns(df)
    assert 'Delivery Days' in df.columns
    assert 'Order Year' in df.columns
    assert 'Order Month' in df.columns
    assert df['Delivery Days'].iloc[0] == 4


def test_detect_outliers_iqr(sample_df):
    outliers, lower, upper = detect_outliers_iqr(sample_df, 'Sales')
    assert isinstance(outliers, pd.DataFrame)
    assert upper > lower