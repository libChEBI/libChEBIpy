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
        self.__typ__ = typ
        self.__accession_number__ = accession_number
        self.__source__ = source

    def get_type(self):
        '''Returns type'''
        return self.__typ__

    def get_accession_number(self):
        '''Returns accession number'''
        return self.__accession_number__

    def get_source(self):
        '''Returns source'''
        return self.__source__
