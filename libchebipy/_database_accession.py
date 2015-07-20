'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._sourced_data import SourcedData as SourcedData

class DatabaseAccession(SourcedData):
    '''COMMENT'''

    def __init__(self, typ, accession_number, source):
        self.__typ__e__ = typ
        self.__accession_number = accession_number
        SourcedData.__init__(self, source)


    def get_type(self):
        '''Returns type'''
        return self.__typ__e__


    def get_accession_number(self):
        '''Returns accession number'''
        return self.__accession_number
