'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject as BaseObject

class Comment(BaseObject):
    '''COMMENT'''

    def __init__(self, datatype_id, datatype, text, created_on):
        self.__datatype___id__ = datatype_id
        self.__datatype__ = datatype
        self.__text__ = text
        self.__created_on__ = created_on
        BaseObject.__init__(self)


    def get_datatype_id(self):
        '''Returns datatype_id'''
        return self.__datatype___id__


    def get_datatype(self):
        '''Returns datatype'''
        return self.__datatype__


    def get_text(self):
        '''Returns text'''
        return self.__text__


    def get_created_on(self):
        '''Returns created_on'''
        return self.__created_on__
