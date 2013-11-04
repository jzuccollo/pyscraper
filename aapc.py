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


    freq_dict = { 'A' : 1., 'Q' : 4., 'M' : 12.}
    freq_offset = { 'A' : pd.datetools.YearEnd(), 'Q' : pd.datetools.QuarterEnd(), 'M' : pd.datetools.MonthEnd()}
    periods = int(yrs * freq_dict[freq])

    cagr = 100 * ((ser[end] / ser[end - periods * freq_offset[freq]]) ** ( 1. / yrs ) - 1.)
    print 'The CAGR for the', yrs, 'years to', month_name[end.month], end.year, 'is', \
            round(cagr, 2), 'per cent per annum.'

    return cagr
