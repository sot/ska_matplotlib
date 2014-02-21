from setuptools import setup
setup(name='Ska.Matplotlib',
      author = 'Tom Aldcroft',
      description='Matplotlib utilities',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      version='0.11',
      zip_safe=False,
      namespace_packages=['Ska'],
      packages=['Ska', 'Ska/Matplotlib'],
      package_dir={'Ska' : 'Ska',
                   'Ska.Matplotlib': 'Ska/Matplotlib'},
      package_data={}
      )
