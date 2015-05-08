import pandas as pd


def cagr(ser, end, freq='A', yrs=4):
    """
    Takes series, returns CAGR

    ser: the pandas series
    end: the final date, as a pandas datetime object
    freq: frequency of series, 'A', 'Q', or 'M'
    yrs: how many years to take the CAGR over, prior to 'end'

    eg. aapc(YBHA, pd.datetime(2013, 9, 31), freq='Q', yrs=2)
    """

    from calendar import month_name

    if isinstance(ser, pd.core.frame.DataFrame):
        ser = ser.squeeze()

    freq_dict = {'A': 1., 'Q': 4., 'M': 12.}
    freq_offset = {'A': pd.datetools.YearEnd(),
                   'Q': pd.datetools.QuarterEnd(),
                   'M': pd.datetools.MonthEnd()}
    periods = int(yrs * freq_dict[freq])

    cagr_val = 100 * \
        ((ser.loc[end] / ser.loc[end - periods * freq_offset[freq]])
         ** (1. / yrs) - 1.)
    print('The CAGR for the {0:} years to {1:} {2:} is {3:0.2f} per cent per annum.'.format(
        yrs, month_name[end.month], end.year, cagr_val))

    return cagr_val


def trend(ser, start, end):
    """Fit exponential trend to series. Useful for adding a trendline
    to charts. Trend can be fit over a subset of values of the series.

            ser: series to fit trend to
            start: date to begin fitting
            end: date to end fitting

        Returns:
            new_ser: fitted trend for entire series."""

    from scipy.optimize import curve_fit
    from numpy import exp

    if isinstance(ser, pd.core.frame.DataFrame):
        ser = ser.squeeze()

    def func(x, a, b, c):
        return a * exp(-b * x) + c

    fitser = ser[start:end]
    xfit = range(fitser.shape[0])
    xall = range(ser.shape[0])
    yn = fitser.values

    popt, _ = curve_fit(func, xfit, yn)

    return pd.Series(data=func(xall, *popt), index=ser.index)


def project(ser, start, end):
    """Fit AR model to series and project to end of index. Primarily
    useful for filling in missing values at the end of time series to
    ensure they match.

            ser: series to fit trend to
            start: date to begin fitting
            end: date to end fitting

        Returns:
            new_ser: series with missing end values replaced by fitted
                     values."""

    from statsmodels.tsa.ar_model import AR

    trend_mod = AR(ser[start:end]).fit()

    return trend_mod.predict(
        start=trend_mod.k_ar, end=ser.index.shape[0])
