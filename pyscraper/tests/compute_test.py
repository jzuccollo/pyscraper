import nose
import pandas as pd
from pyscraper import scrape, compute

# Check that all major scrape calls are returning the right data type
# even though a dataframe s being passed instead of the expected Series
test_frame = scrape.from_ONS('qna', ['YBHA'], 'Q')


def test_cagr_returns_float():
    "Test that compute.cagr returns a float"
    test_val = compute.cagr(test_frame, pd.datetime(2008, 3, 31), freq='Q')
    nose.tools.assert_true(isinstance(test_val, float))


def test_trend_returns_series():
    "Test that compute.trend returns a pandas series"
    test_val = compute.trend(test_frame, pd.datetime(2008, 3, 31),
                             pd.datetime(2014, 12, 31))
    nose.tools.assert_true(isinstance(test_val, pd.core.series.Series))


def test_project_returns_series():
    "Test that compute.project returns a pandas series"
    test_val = compute.project(test_frame, pd.datetime(2008, 3, 31),
                               pd.datetime(2014, 12, 31))
    nose.tools.assert_true(isinstance(test_val, pd.core.series.Series))
