def cagr(ser, end, freq='A', yrs=4):
    """
    Takes series, returns CAGR

    ser: the pandas series
    end: the final date, as a pandas datetime object
    freq: frequency of series, 'A', 'Q', or 'M'
    yrs: how many years to take the CAGR over

    eg. aapc(YBHA, pd.datetime(2013, 9, 31), freq='Q', yrs=2)
    """

    from calendar import month_name
    import pandas as pd

    freq_dict = {'A': 1., 'Q': 4., 'M': 12.}
    freq_offset = {'A': pd.datetools.YearEnd(
    ), 'Q': pd.datetools.QuarterEnd(), 'M': pd.datetools.MonthEnd()}
    periods = int(yrs * freq_dict[freq])

    cagr = 100 * \
        ((ser[end] / ser[end - periods * freq_offset[freq]])
         ** (1. / yrs) - 1.)
    print 'The CAGR for the', yrs, 'years to', month_name[end.month], end.year, 'is', \
        round(cagr, 2), 'per cent per annum.'

    return cagr


def trend(ser, start=pd.datetime(1998, 3, 31), yrs=5):
    """Takes series, returns exponential trend as series."""

    import pandas as pd

    aapc = cagr(ser, start + yrs * pd.DateOffset.year(),
                end, freq='Q', yrs=yrs)
    helper_list = []
    for i in range(len(ser[start:])):
        helper_list.append(ser[start] * aapc ** i)
    return pd.Series(helper_list, index=ser[start:].index)
