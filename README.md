#pydatafuncs

A script to scrape series from the UK Office for National Statistics, Bank of England, and International Monetary Fund. A few utility and computational tools are also included.

## `pydatafuncs.scrape`

Despite the advent of (Quandl)[http://www.quandl.com] there are still many series an analyst will need that are only available in spreadsheets. The functions here will pull your desired time series into a pandas dataframe. There are three core functions in the module:

 - `from_ONS(dataset, series, freq)`
 - `from_BoE(series, datefrom=None, yearsback=5, vpd='y')`
 - `from_IMF(dataset, series=None, countries=None)`

See docstrings for details.
