'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject

class SourcedData(BaseObject):
    '''COMMENT'''

    def __init__(self, source):
        self.__source__ = source


    def get_source(self):
        '''Returns source'''
        return self.__source__
    