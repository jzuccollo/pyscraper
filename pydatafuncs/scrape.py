# -*- coding: utf-8 -*-
# Functions to pull ONS and BoE data series by code and return them as a
# pandas dataframes.

# ONS IMPORTER

import pandas as pd


def _retrieve_ONS_csv(dataset, series):
    """Return csv file with required dataset and series"""
    from urllib2 import urlopen
    # Clean input parameters
    dataset = dataset.lower().strip()
    series = series.upper().replace(" ", "")
    # Grab the raw csv
    target_url = 'http://www.ons.gov.uk/ons/datasets-and-tables/downloads/csv.csv?dataset=' + dataset \
        + '&cdid=' + series
    return urlopen(target_url)


def _create_quarterly_index(dfindex):
    """Takes a pandas dataframe index, '2002 Q2', and returns DatetimeIndex"""

    thedate = dfindex.values[0].split()
    starting_quarter = str(3 * int(thedate[1][-1]))
    starting_year = thedate[0]
    df2index = pd.date_range('1/' + starting_quarter + '/' + starting_year,
                             periods=len(dfindex), freq='Q-DEC')
    return df2index


def _timeseries_index(df, freq):
    """Takes dataframe and converts first column to DateTimeIndex"""
    df2 = df.set_index('Unnamed: 0')
    try:
        df2.index = pd.to_datetime(df2.index, errors='raise')
    except ValueError as e:  # to_datetime can't parse '2010 Q2' dates
        if e.message != "unknown string format":
            raise
        else:
            df2.index = _create_quarterly_index(df2.index)
    return df2


def from_ONS(dataset, series, freq):
    """

    Function to download specific series from the ONS website and return a pandas dataframe. Downloads a csv from the ONS site and parses it.

    Takes:
        dataset: the abbreviated name of the ONS dataset (string). eg. 'qna', 'lms', 'mm23'
        series: ONS series codes to retrieve (string, comma-separated). eg. 'YBHA, ABMI'
        freq: frequency of data required, {'A', 'Q', 'M'}

    Returns:
        df_dict: a dict of three pandas dataframes, 'annual', 'quarterly', and
        'monthly'. Each contains all time series from the dataset in the
        specified frequency.

    Example

    from_ONS('qna', 'YBHA, ABMI', 'Q')
    """

    re_dict = {'Q': '\d{4,4} Q\d$',
               'A': '\d{4,4}$',
               'M': '\d{4,4} [A-Z]{3,3}$'}

    myfile = _retrieve_ONS_csv(dataset, series)
    dfraw = pd.read_csv(myfile)
    criterion = dfraw['Unnamed: 0'].str.contains(re_dict[freq], na=False)
    if dfraw[criterion].empty:
        print "That frequency is unavailable for your series."
        return
    else:
        df = _timeseries_index(dfraw[criterion], freq)
    df = df.astype(float)

    return df


# BoE IMPORTER

def _get_initial_date(yearsback):
    """
    Returns the date yearsback years before today.

    """

    from datetime import datetime

    dt = datetime.now()

    try:
        dt = dt.replace(year=dt.year - yearsback)
    except ValueError:
        dt = dt.replace(year=dt.year - yearsback, day=dt.day - 1)
    return dt


def from_BoE(series, datefrom=None, yearsback=5, vpd='y'):
    """

    Import latest data from the Bank of England website using csv interface.

    Takes:
        series: BoE series name (comma-separated strings)
        datefrom: Initial date of series (date string, 'DD/MON/YYYY')
        yearsback: If datefrom is not specified, how many years of data would you like, counting backwards from today?

    Returns:
        df: Pandas dataframe of time series

    eg. df = importBoE('LPMAUZI,LPMAVAA', datefrom='01/Oct/2007 ')


    Optional arguments:

       vpd:	Include provisional data? ('Y' or 'N')

    """

    import pandas as pd

    Datefrom = datefrom if datefrom is not None else _get_initial_date(
        yearsback)
    Dateto = 'now'
    SeriesCodes = series
    UsingCodes = 'Y'
    CSVF = 'TN'
    VPD = vpd

    url = 'http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?csv.x=yes&Datefrom=' + Datefrom \
        + '&Dateto=' + Dateto \
        + '&SeriesCodes=' + SeriesCodes \
        + '&UsingCodes=' + UsingCodes \
        + '&CSVF=' + CSVF \
        + '&VPD=' + VPD

    return pd.read_csv(url, index_col=0, parse_dates=True, header=0)
