from setuptools import setup

from Ska.Matplotlib import __version__

setup(name='Ska.Matplotlib',
      author='Tom Aldcroft',
      description='Matplotlib utilities',
      author_email='taldcroft@cfa.harvard.edu',
      version=__version__,
      zip_safe=False,
      packages=['Ska', 'Ska.Matplotlib'],
      )
