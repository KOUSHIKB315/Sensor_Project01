from setuptools import find_packages, setup  #setuptools is a package development and distribution library for Python. It provides tools for packaging Python projects, managing dependencies, and distributing them to the Python Package Index (PyPI) or other repositories.

#setup() is a function provided by setuptools that is used to define the metadata and configuration for a Python package. It takes various arguments that specify the package name, version, author, description, dependencies, and other information.
from typing import List

HYPHEN_E_DOT= '-e.'
def get_requirements(file_path: str)-> List[str]:
  requirements=[]
  with open(file_path) as file_obj:
    requirements=file_obj.readlines()
    requirements= [req.replace('\n','') for req in requirements]
  
  if HYPHEN_E_DOT in requirements:
    requirements.remove(HYPHEN_E_DOT)
  return requirements 

setup(
  name= 'Fault detection',
  version ='0.0.1',
  author='KoushikBandyopadhyay',
  author_email= 'koushikbandyopadhyay3152003@gmail.com',
  install_requirements= get_requirements('requirements.txt'),    # the user defined function will read the requirements.txt file and return a list of dependencies that will be installed when the package is installed.
  packages= find_packages()
)
