'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
from libchebipy._base_object import BaseObject as BaseObject


class CompoundOrigin(BaseObject):
    '''Class representing a ChEBI compound origin.'''

    def __init__(self, species_text, species_accession, component_text,
                 component_accession, strain_text, strain_accession,
                 source_type, source_accession, comments):
        self.__species_text__ = None if species_text == 'null' \
            else species_text
        self.__species_accession__ = None if species_accession == 'null' \
            else species_accession
        self.__component_text__ = None if component_text == 'null' \
            else component_text
        self.__component_accession__ = None if component_accession == 'null' \
            else component_accession
        self.__strain_text__ = None if strain_text == 'null' \
            else strain_text
        self.__strain_accession__ = None if strain_accession == 'null' \
            else strain_accession
        self.__source_type__ = None if source_type == 'null' \
            else source_type
        self.__source_accession__ = None if source_accession == 'null' \
            else source_accession
        self.__comments__ = None if comments == 'null' else comments
        BaseObject.__init__(self)

    def get_species_text(self):
        '''Returns species_text'''
        return self.__species_text__

    def get_species_accession(self):
        '''Returns species_accession'''
        return self.__species_accession__

    def get_component_text(self):
        '''Returns component_text'''
        return self.__component_text__

    def get_component_accession(self):
        '''Returns component_accession'''
        return self.__component_accession__

    def get_strain_text(self):
        '''Returns strain_text'''
        return self.__strain_text__

    def get_strain_accession(self):
        '''Returns strain_accession'''
        return self.__strain_accession__

    def get_source_type(self):
        '''Returns source_type'''
        return self.__source_type__

    def get_source_accession(self):
        '''Returns source_accession'''
        return self.__source_accession__

    def get_comments(self):
        '''Returns comments'''
        return self.__comments__
