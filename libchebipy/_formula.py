'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._sourced_data import SourcedData as SourcedData

class Formula(SourcedData):
    '''COMMENT'''

    def __init__(self, formula, source):
        self.__formula = formula
        SourcedData.__init__(self, source)


    def get_formula(self):
        '''Returns formula'''
        return self.__formula
