# Licensed under a 3-clause BSD style license - see LICENSE.rst
from setuptools import setup
from ska_helpers.setup_helper import duplicate_package_info

name = "ska_matplotlib"
namespace = "Ska.Matplotlib"

packages = ["ska_matplotlib"]
package_dir = {name: name}

duplicate_package_info(packages, name, namespace)
duplicate_package_info(package_dir, name, namespace)

setup(name=name,
      author='Tom Aldcroft',
      description='Matplotlib utilities',
      author_email='taldcroft@cfa.harvard.edu',
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      zip_safe=False,
      package_dir=package_dir,
      packages=packages,
      )
