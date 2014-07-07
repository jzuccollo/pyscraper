#pyscraper

A script to scrape series from the UK Office for National Statistics, Bank of England, and International Monetary Fund. A few utility and computational tools are also included.

## Installation

Unpack the tarball and install with `python setup.py install`.

## `scrape` module

Despite the advent of [Quandl](http://www.quandl.com) there are still many series an analyst will need that are only available in spreadsheets. The functions here will pull your desired time series into a pandas dataframe. There are three core functions in the module:

 - `from_ONS(dataset, series, freq)`: Scrapes the CSV files on [the ONS website](http://www.ons.gov.uk/ons/datasets-and-tables/index.html?content-type=Dataset&pubdateRangeType=allDates&sortBy=pubdate&sortDirection=DESCENDING&newquery=*&pageSize=50&applyFilters=true&content-type-orig=%22Dataset%22+OR+content-type_original%3A%22Reference+table%22).
 - `from_BoE(series, datefrom=None, yearsback=5, vpd='y')`: Scrapes from the Bank of England's [Interactive Database](http://www.bankofengland.co.uk/boeapps/iadb/newintermed.asp).
 - `from_IMF(dataset, series=None, countries=None)`: Scrapes the IMF's [World Economic Outlook](http://www.imf.org/external/ns/cs.aspx?id=29) and [Public Finances in Modern History Database](http://www.imf.org/external/np/fad/histdb/).

See docstrings for syntax details.

## `deseasonalise` module

Python wrapper on X-13ARIMA-SEATS to deseasonalise time series data. Takes and returns a `pandas` dataframe. Requires [X-13ARIMA-SEATS](https://www.census.gov/srd/www/x13as/) executable to be installed. Module has one function, `deseasonalise`, which takes either a dataframe or series and returns the same adjusted.

Note that the path to X-13 is hardcoded in `deseasonalise.py` as `C:/Program Files (x86)/winx13/x13as/x13as.exe`.
