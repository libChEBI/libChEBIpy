'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from setuptools import find_packages, setup

setup(name='libChEBIpy',
      version='1.0.1',
      description='libChEBIpy: a Python API for accessing the ChEBI database',
      long_description='libChEBIpy: a Python API for accessing the ChEBI ' +
      'database',
      url='http://github.com/synbiochem/libChEBIpy',
      author='Neil Swainston',
      author_email='neil.swainston@manchester.ac.uk',
      license='MIT',
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Build Tools',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7'
                   ],
      keywords='chemistry cheminformatics ChEBI',
      packages=find_packages(),
      test_suite='libchebipy.test')
