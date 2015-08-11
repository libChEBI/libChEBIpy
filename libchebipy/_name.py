'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject as BaseObject


class Name(BaseObject):
    '''Class representing a ChEBI name.'''

    def __init__(self, name, typ, source, adapted, language):
        self.__name = name
        self.__typ = typ
        self.__source = source
        self.__adapted = adapted
        self.__language = language

    def get_name(self):
        '''Returns name'''
        return self.__name

    def get_type(self):
        '''Returns type'''
        return self.__typ

    def get_adapted(self):
        '''Returns adapted'''
        return self.__adapted

    def get_language(self):
        '''Returns language'''
        return self.__language

    def get_source(self):
        '''Returns source'''
        return self.__source
