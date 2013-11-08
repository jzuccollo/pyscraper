# -*- coding: utf-8 -*-

# Author: James Zuccollo
# Last revision: 24 October 2013

# Functions to pull ONS and BoE data series by code and return them as a pandas dataframes.

def ONSimport(dataset, series):
    """

    Function to download specific series from the ONS website and return a pandas dataframe. Downloads a csv from the ONS site and parses it.

    Takes:
        dataset: the abbreviated name of the ONS dataset (string). eg. 'qna', 'lms', 'mm23'
        series: ONS series codes to retrieve (string, comma-separated). eg. 'YBHA, ABMI'

    Returns:
        df_dict: a dict of three pandas dataframes, 'annual', 'quarterly', and
        'monthly'. Each contains all time series from the dataset in the
        specified frequency.

    Example

    ONSimport('qna', 'YBHA, ABMI')
    """

    import csv
    import urllib2
    import re
    import numpy as np
    import pandas as pd


    # Clean input parameters
    dataset = dataset.lower().strip()
    series = series.upper().replace(" ", "")

    # Grab the raw csv
    target_url = 'http://www.ons.gov.uk/ons/datasets-and-tables/downloads/csv.csv?dataset=' + dataset \
            + '&cdid=' + series
    myfile = urllib2.urlopen(target_url)
    mycsv = csv.reader(myfile)

    # Move the csv to a list of lists
    wholecsv = []
    for row in mycsv:
        wholecsv.append(row)
    myfile.close()

    # Extract the series names
    headers = wholecsv[0][1:]

    # Find the first blank row, denoting the end of the data
    blankrow = [index for index, line in enumerate(wholecsv) if line == []][0]
    data = wholecsv[1:blankrow]

    # Grab the names of the series
    metadata = {}
    for series in headers:
        for index, line in enumerate(wholecsv):
            try:
                if line[0].find(series) >= 0:
                    metadata[line[0]] = line[1]
            except:
                print 'Skipping line', index, 'in metadata search'
    # Split the data into annual/monthly/quarterly

    # Compile regular expressions to split the dates
    quarterly_re = re.compile('\d{4,4} Q\d$')
    annual_re = re.compile('\d{4,4}$')
    monthly_re = re.compile('\d{4,4} [A-Z]{3,3}$')

    # Create separate lists for each dataset
    quarterly_data = []
    monthly_data = []
    annual_data = []

    for line in data:
        if annual_re.match(line[0]): annual_data.append(line)
        elif quarterly_re.match(line[0]): quarterly_data.append(line)
        elif monthly_re.match(line[0]): monthly_data.append(line)
        else: print line, 'cannot be sorted.'

    # Reshape the lists into pandas dataframes
    def transposed(lists):
        """Transpose lists of data"""
        if not lists: return []
        return map(lambda *row: list(row), *lists)


    def cleaner(seq):
        """Convert list to floats and np.nans"""
        for x in seq:
            try:
                yield float(x)
            except ValueError:
                yield np.NaN


    def to_df(dat):
        """Convert list of lists to pandas dataframe"""
        int_series = transposed(dat)
        index_list = int_series[0]
        clean_data_lists = [list(cleaner(l)) for l in  int_series[1:]]
        return pd.DataFrame(dict(zip(headers, clean_data_lists)), index=index_list, dtype=np.float64)


    df_dict = {}
    for dat in [('annual', annual_data), ('monthly', monthly_data), ('quarterly', quarterly_data)]:
        try:
            df_dict[dat[0]] = to_df(dat[1])
        except:
            print 'The', dat[0], 'frequency failed to convert to a dataframe. It may be missing for this ONS series'

    # Convert the indices to time series
    def start_year(df):
        return df.index.values[0][:4]

    ## Quarterly
    try:
        qmnth = str(3 * int(df_dict['quarterly'].index.values[0][-1]))
        df_dict['quarterly'].index = pd.date_range('1/'+qmnth+'/'+start_year(df_dict['quarterly']), \
                                               periods=len((df_dict['quarterly'])), freq='Q-DEC')
    except:
        print 'Error indexing quarterly data. It may not exist for this series.'

    ## Annual
    try:
        df_dict['annual'].index = pd.date_range(start_year(df_dict['annual']), \
                                               periods=len((df_dict['annual'])), freq='A')
    except:
        print 'Error indexing annual data. It may not exist for this series.'
    ## Monthly
    try:
        from calendar import month_abbr
        month_dict = {v.upper() : k for k,v in enumerate(month_abbr)}
        mmonth = df_dict['monthly'].index[0][-3:]
        df_dict['monthly'].index = pd.date_range('28/'+str(month_dict[mmonth])+'/'+start_year(df_dict['monthly']), \
                                               periods=len((df_dict['monthly'])), freq='M')
    except:
        print 'Error indexing monthly data. It may not exist for this series.'

    return df_dict



def BoEimport(series, datefrom, vpd='y'):
    """

    Import latest data from the Bank of England website using csv interface.

    Takes:
        series: BoE series name (comma-separated strings)
        datefrom: Initial date of series (date string, 'DD/MON/YYYY')

    Returns:
        df: Pandas dataframe of time series

    eg. df = importBoE('LPMAUZI,LPMAVAA', '01/Oct/2007 ')


    Optional arguments:

       vpd:	Include provisional data? ('Y' or 'N')

    """

    import pandas as pd


    Datefrom = datefrom
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


def quandl_ons_cleaner(dfql):
    """Take a Quandl dataframe from the UKONS repo and make sense of the names"""
    colnames = []
    print 'Originally imported names are', dfql.columns.values

    import re

    for name in dfql.columns.values:
        try:
            colnames.append(re.search('UKONS\.[A-Z]{4,4} ', name).group(0)[-5:-1])
        except AttributeError:
            colnames.append(re.search('UKONS\.[A-Z]*_[A-Z]{4,4}', name).group(0)[-4:])
        else:
            pass

    print 'New column names to be assigned are', colnames
    dfql.columns = colnames

    return dfql
