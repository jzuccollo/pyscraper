import nose
import pandas as pd
from pydatafuncs import scrape

# Check that all major scrape calls are returning the right data type


def test_from_ONS_returns_dataframe():
    "Test that scrape.from_ONS returns a pandas dataframe"
    test_frame = scrape.from_ONS('qna', ['YBHA', 'ABMI'], 'Q')
    nose.tools.assert_true(type(test_frame) == pd.core.frame.DataFrame)


def test_from_BoE_returns_dataframe():
    "Test that scrape.from_BoE returns a pandas dataframe"
    test_frame = scrape.from_BoE(
        ['LPMAUZI', 'LPMAVAA'], datefrom=pd.datetime(2007, 8, 1))
    nose.tools.assert_true(type(test_frame) == pd.core.frame.DataFrame)


def test_from_weo_returns_panel():
    "Test that scrape.from_IMF returns a pandas panel on the WEO dataset"
    test_frame = scrape.from_IMF(
        'weo', series=['GGSB_NPGDP', 'GGX_NGDP'], countries=['United Kingdom'])
    nose.tools.assert_true(type(test_frame) == pd.core.panel.Panel)


def test_from_pubfin_returns_panel():
    "Test that scrape.from_IMF returns a pandas panel on the Public Finances dataset"
    test_frame = scrape.from_IMF(
        'pubfin', series=['rev', 'prim_exp'], countries=['United Kingdom'])
    nose.tools.assert_true(type(test_frame) == pd.core.panel.Panel)
