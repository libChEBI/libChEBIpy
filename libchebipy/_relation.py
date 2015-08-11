'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject as BaseObject


class Relation(BaseObject):
    '''Class representing a ChEBI relation.'''

    def __init__(self, typ, target_chebi_id, status):
        self.__typ = typ
        self.__target_chebi_id = target_chebi_id
        self.__status = status
        BaseObject.__init__(self)

    def get_type(self):
        '''Returns type'''
        return self.__typ

    def get_target_chebi_id(self):
        '''Returns target_chebi_id'''
        return self.__target_chebi_id

    def get_status(self):
        '''Returns status'''
        return self.__status
