from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pydatafuncs',
      version='0.1.0',
      description='Useful time series importation and manipulation functions',
      url='http://github.com/jzuccollo/pydatafuncs',
      author='jzuccollo',
      author_email='james.zuccollo@reform.co.uk',
      license='MIT',
      packages=['pydatafuncs'],
      install_requires=[
          'pandas', 'csv', 'urllib2', 're', 'numpy', 'calendar'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False,
      include_package_data=True)
