'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import math

from libchebipy._base_object import BaseObject

from libchebipy._parsers import _get_all_comments, _get_all_compound_origins, \
    _get_all_database_accessions, _get_all_formulae, _get_all_ids, \
    _get_all_incomings, _get_all_modified_on, _get_all_names, \
    _get_all_outgoings, _get_charge, _get_created_by, _get_definition, \
    _get_inchi_key, _get_inchi, _get_mass, _get_mol_filename, _get_mol, \
    _get_name, _get_parent_id, _get_references, _get_smiles, _get_source, \
    _get_star, _get_status


class ChebiException(Exception):
    '''COMMENT'''
    pass


class ChebiEntity(BaseObject):
    '''Class representing a single entity in the ChEBI database.'''

    def __init__(self, chebi_id):
        self.__chebi_id__ = chebi_id
        self.__all_ids__ = None

        if self.get_name() is None:
            raise ChebiException('ChEBI id ' + str(chebi_id) + ' invalid')

    def get_id(self):
        '''Returns id'''
        return self.__chebi_id__

    def get_parent_id(self):
        '''Returns parent id'''
        return _get_parent_id(self.__chebi_id__)

    def get_formulae(self):
        '''Returns formulae'''
        return _get_all_formulae(self._get_all_ids())

    def get_formula(self):
        '''Returns formula'''
        formulae = self.get_formulae()
        return None if len(formulae) == 0 else formulae[0].get_formula()

    def get_mass(self):
        '''Returns mass'''
        mass = _get_mass(self.__chebi_id__)

        if math.isnan(mass):
            mass = _get_mass(self.get_parent_id())

        if math.isnan(mass):
            for parent_or_child_id in self._get_all_ids():
                mass = _get_mass(parent_or_child_id)

                if not math.isnan(mass):
                    break

        return mass

    def get_charge(self):
        '''Returns charge'''
        charge = _get_charge(self.__chebi_id__)

        if math.isnan(charge):
            charge = _get_charge(self.get_parent_id())

        if math.isnan(charge):
            for parent_or_child_id in self._get_all_ids():
                charge = _get_charge(parent_or_child_id)

                if not math.isnan(charge):
                    break

        return charge

    def get_comments(self):
        '''Returns comments'''
        return _get_all_comments(self._get_all_ids())

    def get_source(self):
        '''Returns source'''
        return _get_source(self.__chebi_id__)

    def get_name(self):
        '''Returns name'''
        name = _get_name(self.__chebi_id__)

        if name is None:
            name = _get_name(self.get_parent_id())

        if name is None:
            for parent_or_child_id in self._get_all_ids():
                name = _get_name(parent_or_child_id)

                if name is not None:
                    break

        return name

    def get_definition(self):
        '''Returns definition'''
        definition = _get_definition(self.__chebi_id__)

        if definition is None:
            definition = _get_definition(self.get_parent_id())

        if definition is None:
            for parent_or_child_id in self._get_all_ids():
                definition = _get_definition(parent_or_child_id)

                if definition is not None:
                    break

        return definition

    def get_modified_on(self):
        '''Returns modified on'''
        return _get_all_modified_on(self._get_all_ids())

    def get_created_by(self):
        '''Returns created by'''
        created_by = _get_created_by(self.__chebi_id__)

        if created_by is None:
            created_by = _get_created_by(self.get_parent_id())

        if created_by is None:
            for parent_or_child_id in self._get_all_ids():
                created_by = _get_created_by(parent_or_child_id)

                if created_by is not None:
                    break

        return created_by

    def get_star(self):
        '''Returns star'''
        return _get_star(self.__chebi_id__)

    def get_database_accessions(self):
        '''Returns database accessions'''
        return _get_all_database_accessions(self._get_all_ids())

    def get_inchi(self):
        '''Returns inchi'''
        inchi = _get_inchi(self.__chebi_id__)

        if inchi is None:
            inchi = _get_inchi(self.get_parent_id())

        if inchi is None:
            for parent_or_child_id in self._get_all_ids():
                inchi = _get_inchi(parent_or_child_id)

                if inchi is not None:
                    break

        return inchi

    def get_inchi_key(self):
        '''Returns inchi key'''
        structure = _get_inchi_key(self.__chebi_id__)

        if structure is None:
            structure = _get_inchi_key(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self._get_all_ids():
                structure = _get_inchi_key(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_smiles(self):
        '''Returns smiles'''
        structure = _get_smiles(self.__chebi_id__)

        if structure is None:
            structure = _get_smiles(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self._get_all_ids():
                structure = _get_smiles(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_mol(self):
        '''Returns mol'''
        structure = _get_mol(self.__chebi_id__)

        if structure is None:
            structure = _get_mol(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self._get_all_ids():
                structure = _get_mol(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_mol_filename(self):
        '''Returns mol filename'''
        mol_filename = _get_mol_filename(self.__chebi_id__)

        if mol_filename is None:
            mol_filename = _get_mol_filename(self.get_parent_id())

        if mol_filename is None:
            for parent_or_child_id in self._get_all_ids():
                mol_filename = \
                    _get_mol_filename(parent_or_child_id)

                if mol_filename is not None:
                    break

        return mol_filename

    def get_names(self):
        '''Returns names'''
        return _get_all_names(self._get_all_ids())

    def get_references(self):
        '''Returns references'''
        return _get_references(self._get_all_ids())

    def get_compound_origins(self):
        '''Returns compound origins'''
        return _get_all_compound_origins(self._get_all_ids())

    def get_outgoings(self):
        '''Returns outgoings'''
        return _get_all_outgoings(self._get_all_ids())

    def get_incomings(self):
        '''Returns incomings'''
        return _get_all_incomings(self._get_all_ids())

    def _get_status(self):
        '''Returns status'''
        return _get_status(self.__chebi_id__)

    def _get_all_ids(self):
        '''Returns all ids'''
        if self.__all_ids__ is None:
            parent_id = self.get_parent_id()
            self.__all_ids__ = _get_all_ids(self.__chebi_id__
                                            if math.isnan(parent_id)
                                            else parent_id)

            if self.__all_ids__ is None:
                self.__all_ids__ = []

        return self.__all_ids__
