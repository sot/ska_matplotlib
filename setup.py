# Licensed under a 3-clause BSD style license - see LICENSE.rst
from setuptools import setup

setup(name='Ska.Matplotlib',
      author='Tom Aldcroft',
      description='Matplotlib utilities',
      author_email='taldcroft@cfa.harvard.edu',
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      zip_safe=False,
      packages=['Ska', 'Ska.Matplotlib'],
      )
