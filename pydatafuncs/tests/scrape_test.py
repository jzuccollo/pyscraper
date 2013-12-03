import nose

def setup_module():
	import pandas as pd
	import numpy as np
	pass


def from_ONS_setup():
	pass


def from_ONS_teardown():
	pass


@nose.with_setup(from_ONS_setup, from_ONS_teardown)
def test_from_ONS1():
	print "Testing scrape.from_ONS..."
	from pydatafuncs import scrape

	nose.tools.assert_equals(scrape.from_ONS(dataset, series, frequency), 1)