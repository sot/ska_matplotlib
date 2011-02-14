from setuptools import setup
setup(name='Ska.Matplotlib',
      author = 'Tom Aldcroft',
      description='Matplotlib utilities',
      author_email = 'taldcroft@cfa.harvard.edu',
      py_modules = ['Ska.Matplotlib'],
      version='0.07',
      zip_safe=False,
      namespace_packages=['Ska'],
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
