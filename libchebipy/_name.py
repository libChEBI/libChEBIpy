'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._sourced_data import SourcedData as SourcedData

class Name(SourcedData):
    '''COMMENT'''

    def __init__(self, name, typ, source, adapted, language):
        self.__name__ = name
        self.__typ__e__ = typ
        self.__adapted__ = adapted
        self.__language__ = language
        SourcedData.__init__(self, source)


    def get_name(self):
        '''Returns name'''
        return self.__name__


    def get_type(self):
        '''Returns type'''
        return self.__typ__e__


    def get_adapted(self):
        '''Returns adapted'''
        return self.__adapted__


    def get_language(self):
        '''Returns language'''
        return self.__language__
