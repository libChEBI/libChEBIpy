'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject as BaseObject


class DatabaseAccession(BaseObject):
    '''Class representing a ChEBI database accession.'''

    def __init__(self, typ, accession_number, source):
        self.__typ = typ
        self.__accession_number = accession_number
        self.__source = source

    def get_type(self):
        '''Returns type'''
        return self.__typ

    def get_accession_number(self):
        '''Returns accession number'''
        return self.__accession_number

    def get_source(self):
        '''Returns source'''
        return self.__source
