import nose


def setup_module():
    print "Setting up nosetests harness..."
    import pandas as pd
    import numpy as np
    pass


def from_ONS_setup():
    print "Setting up scrape.from_ONS harness..."
    pass


def from_ONS_teardown():
    print "Tearing down scrape.from_ONS harness..."
    pass


@nose.with_setup(from_ONS_setup, from_ONS_teardown)
def test_from_ONS1():
    print "Testing scrape.from_ONS..."
    from pydatafuncs import scrape

    nose.tools.assert_equals(scrape.from_ONS(dataset, series, frequency), 1)
