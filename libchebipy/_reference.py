'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject as BaseObject

class Reference(BaseObject):
    '''COMMENT'''

    def __init__(self, reference_id, reference_db_name, location_in_ref=None,
                 reference_name=None):
        self.__reference_id__ = reference_id
        self.__reference_db_name__ = reference_db_name
        self.__location_in_ref__ = location_in_ref
        self.__reference_name__ = reference_name
        BaseObject.__init__(self)


    def get_reference_id(self):
        '''Returns reference_id'''
        return self.__reference_id__


    def get__reference_db_name(self):
        '''Returns _reference_db_name'''
        return self.__reference_db_name__


    def get_location_in_ref(self):
        '''Returns location_in_ref'''
        return self.__location_in_ref__


    def get_reference_name(self):
        '''Returns reference_name'''
        return self.__reference_name__
