from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pyscraper',
      version='0.2.0',
      description='Time series importation and manipulation functions',
      long_description=open('README.md').read(),
      url='http://github.com/jzuccollo/pyscraper',
      author='jzuccollo',
      author_email='james.zuccollo@reform.co.uk',
      license='MIT',
      packages=['pyscraper'],
      install_requires=[
          'pandas', 'numpy', 'requests', 'matplotlib'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False,
      package_data={'pyscraper': ['templates/template.spc']})
