'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from setuptools import setup

setup(name='libChEBIpy',
      version='1.0',
      description='libChEBIpy: a Python API for accessing the ChEBI database',
      url='http://github.com/neilswainston/libChEBIpy',
      author='Neil Swainston',
      author_email='neil.swainston@manchester.ac.uk',
      license='MIT',
      packages=['libchebipy'],
      test_suite='libchebipy.test'
)
