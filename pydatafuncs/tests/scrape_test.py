import nose
import pandas as pd
import numpy as np
from pydatafuncs import scrape


in_set_a = pd.Index(['2002', '2003', '2004', '2005'])
in_set_q = pd.Index(['2002 Q2', '2002 Q3', '2002 Q4', '2003 Q1'])
in_set_m = pd.Index(['2002 JAN', '2002 FEB', '2002 MAR', '2002 APR'])
in_dat = pd.DataFrame({'ser1': np.ones(4), 'ser2': 2 * np.ones(4)})


def test_create_quarterly_index1():
    """Quarterly produces quarterly"""
    gen_out_set = scrape._create_quarterly_index(in_set_q)
    reqd_out_set = pd.date_range('1/6/2002', periods=4, freq='Q-DEC')
    nose.tools.assert_true(all(reqd_out_set == gen_out_set))


def test_timeseries_index1():
    """Annual first column creates annual index"""
    gen_in_set = in_dat
    gen_in_set['Unnamed: 0'] = in_set_a.values
    reqd_out_set = pd.date_range('1/6/2002', periods=4, freq='A')
    gen_out_set = scrape._timeseries_index(gen_in_set, 'A')
    nose.tools.assert_true(all(reqd_out_set == gen_out_set.index))


def test_timeseries_index2():
    """Quarterly first column creates quarterly index"""


def test_timeseries_index3():
    """Monthly first column creates monthly index"""
