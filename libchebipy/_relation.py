'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from ._base_object import BaseObject


class Relation(BaseObject):
    '''Class representing a ChEBI relation.'''

    def __init__(self, typ, target_chebi_id, status):
        self.__typ = typ
        self.__target_chebi_id = int(target_chebi_id.replace('CHEBI:', ''))
        self.__status = status
        BaseObject.__init__(self)

    def get_type(self):
        '''Returns type'''
        return self.__typ

    def get_target_chebi_id(self):
        '''Returns target_chebi_id'''
        return 'CHEBI:' + str(self.__target_chebi_id)

    def __get_status(self):
        '''Returns status'''
        return self.__status
