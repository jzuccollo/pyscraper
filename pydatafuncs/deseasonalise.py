# Module to call X-13 ARIMA-SEATS and return an adjusted series

import errno
import shutil
import tempfile
import os
import pandas as pd
from subprocess import Popen, PIPE
from numpy import transpose
from string import Template


# Create .dat file from pandas dataframe
def _make_data(name, ser, freq):
    """Write an X-13 data file"""

    tmpdf = pd.DataFrame.from_records(transpose([ser.index.year,
                                                 ser.index.month * freq / 12]))
    tmpdf['vals'] = ser.values
    tmpdf.dropna().to_csv(name + '.dat', sep='\t', header=False, index=False)


# Create .spc file from template.spc
def _make_spec(name, freq,  **kwargs):
    """Write an X-13 spec file"""

    from pkg_resources import resource_stream

    spec_template = resource_stream(__name__, 'templates/template.spc')
    with spec_template as filein:
        src = Template(filein.read())
    subs_dict = {'dat_file': '"' + name + '.dat"',
                 'period': freq,
                 'outliers': 'AO LS'}
    for key, value in kwargs.iteritems():
        subs_dict[key] = value
    result = src.substitute(subs_dict)
    with open(name + ".spc", "w") as spec_file:
        spec_file.write(result)


# Create .mta file
def _make_meta(name):
    """Write an X-13 meta file"""

    with open(name + ".mta", "w") as meta_file:
        meta_file.write(name)


# Run X-13 ARIMA-SEATS
def _run_x13(name):
    """Run the X-13 meta file written previously in the temp directory"""

    x13_programme = os.path.normpath(
        "C:/Program Files (x86)/winx13/x13as/x13as.exe")
    process = Popen([x13_programme, "-m", name],
                    stdout=PIPE,
                    stderr=PIPE)
    out, err = process.communicate()
    return out, err


# Read output into pandas dataframe
def _parse(x):
    """Custom date-parsing function to read X-13 results file"""

    from calendar import monthrange

    yr = int(str(x)[:4])
    mnth = 3 * int(str(x)[-2:])
    day = monthrange(yr, mnth)[1]
    return pd.datetime(yr, mnth, day)


def _read_results(name):
    """Read the X-13 results into a pandas dataframe"""

    return pd.read_table(name + '.d11',
                         index_col=0,
                         parse_dates=True,
                         date_parser=_parse,
                         header=None,
                         skiprows=2)


def _deseas_series(ser, freq, **kwargs):
    """Create a temp directory, run operations in it and clean up"""

    name = 'x13_tmpfile'
    try:
        tmp_dir = tempfile.mkdtemp()
        curr_dir = os.getcwd()
        os.chdir(tmp_dir)
        _make_data(name, ser, freq)
        _make_spec(name, freq, **kwargs)
        _make_meta(name)
        output, errors = _run_x13(name)
        results = _read_results(name)
    except Exception as e:
        print e
        with open(name + '.err', 'r') as fin:
            print fin.read()
        results = None
    finally:
        try:
            os.chdir(curr_dir)
            shutil.rmtree(tmp_dir)  # delete directory
        except OSError as exc:
            if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                raise  # re-raise exception
    return results


def deseasonalise(df, freq, **kwargs):
    """
    Remove seasonality from time series using X-13.

    Takes:
        df: pandas dataframe or series
        freq: frequency of data in (1, 4, 12)
        kwargs: dictionary of spec options to pass to X-13. Currently
                supports 'outliers'.

    Returns:
        df: pandas dataframe of seasonally adjusted series
    """
    if type(df) == pd.core.frame.DataFrame:
        ds_dict = {}
        for name, ser in df.iteritems():
            print "Processing", name, "\n"
            ds_dict[name] = _deseas_series(ser, freq, **kwargs)
        ds_df = pd.concat(ds_dict, axis=1)
        ds_df.columns = ds_df.columns.droplevel(level=1)
        return ds_df
    elif type(df) == pd.core.series.Series:
        return _deseas_series(df, freq)
    else:
        print("Not a pandas dataframe or series.")
