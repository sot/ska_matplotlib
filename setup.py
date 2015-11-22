from setuptools import setup

from Ska.Matplotlib import __version__

setup(name='Ska.Matplotlib',
      author = 'Tom Aldcroft',
      description='Matplotlib utilities',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      version=__version__,
      zip_safe=False,
      packages=['Ska', 'Ska/Matplotlib'],
      package_dir={'Ska' : 'Ska',
                   'Ska.Matplotlib': 'Ska/Matplotlib'},
      package_data={}
      )
