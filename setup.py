from setuptools import setup
setup(name='Ska.Matplotlib',
      author = 'Tom Aldcroft',
      description='Matplotlib utilities',
      author_email = 'taldcroft@cfa.harvard.edu',
      py_modules = ['Ska.Matplotlib'],
      scripts=['bin/histtest.py',],
      version='0.06',
      zip_safe=False,
      namespace_packages=['Ska'],
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
