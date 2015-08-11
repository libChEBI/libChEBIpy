'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject as BaseObject


class Formula(BaseObject):
    '''Class representing a ChEBI formula.'''

    def __init__(self, formula, source):
        self.__formula = formula
        self.__source = source

    def get_formula(self):
        '''Returns formula'''
        return self.__formula

    def get_source(self):
        '''Returns source'''
        return self.__source
