'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=too-many-public-methods
import math

from libchebipy._base_object import BaseObject
import libchebipy._parsers as parsers


class ChebiException(Exception):
    '''COMMENT'''
    pass


class ChebiEntity(BaseObject):
    '''Class representing a single entity in the ChEBI database.'''

    def __init__(self, chebi_id):
        self.__chebi_id = chebi_id
        self.__all_ids = None

        if self.get_name() is None:
            raise ChebiException('ChEBI id ' + str(chebi_id) + ' invalid')

    def get_id(self):
        '''Returns id'''
        return self.__chebi_id

    def get_parent_id(self):
        '''Returns parent id'''
        return parsers.get_parent_id(self.__chebi_id)

    def get_formulae(self):
        '''Returns formulae'''
        return parsers.get_all_formulae(self.__get_all_ids())

    def get_formula(self):
        '''Returns formula'''
        formulae = self.get_formulae()
        return None if len(formulae) == 0 else formulae[0].get_formula()

    def get_mass(self):
        '''Returns mass'''
        mass = parsers.get_mass(self.__chebi_id)

        if math.isnan(mass):
            mass = parsers.get_mass(self.get_parent_id())

        if math.isnan(mass):
            for parent_or_child_id in self.__get_all_ids():
                mass = parsers.get_mass(parent_or_child_id)

                if not math.isnan(mass):
                    break

        return mass

    def get_charge(self):
        '''Returns charge'''
        charge = parsers.get_charge(self.__chebi_id)

        if math.isnan(charge):
            charge = parsers.get_charge(self.get_parent_id())

        if math.isnan(charge):
            for parent_or_child_id in self.__get_all_ids():
                charge = parsers.get_charge(parent_or_child_id)

                if not math.isnan(charge):
                    break

        return charge

    def get_comments(self):
        '''Returns comments'''
        return parsers.get_all_comments(self.__get_all_ids())

    def get_source(self):
        '''Returns source'''
        return parsers.get_source(self.__chebi_id)

    def get_name(self):
        '''Returns name'''
        name = parsers.get_name(self.__chebi_id)

        if name is None:
            name = parsers.get_name(self.get_parent_id())

        if name is None:
            for parent_or_child_id in self.__get_all_ids():
                name = parsers.get_name(parent_or_child_id)

                if name is not None:
                    break

        return name

    def get_definition(self):
        '''Returns definition'''
        definition = parsers.get_definition(self.__chebi_id)

        if definition is None:
            definition = parsers.get_definition(self.get_parent_id())

        if definition is None:
            for parent_or_child_id in self.__get_all_ids():
                definition = parsers.get_definition(parent_or_child_id)

                if definition is not None:
                    break

        return definition

    def get_modified_on(self):
        '''Returns modified on'''
        return parsers.get_all_modified_on(self.__get_all_ids())

    def get_created_by(self):
        '''Returns created by'''
        created_by = parsers.get_created_by(self.__chebi_id)

        if created_by is None:
            created_by = parsers.get_created_by(self.get_parent_id())

        if created_by is None:
            for parent_or_child_id in self.__get_all_ids():
                created_by = parsers.get_created_by(parent_or_child_id)

                if created_by is not None:
                    break

        return created_by

    def get_star(self):
        '''Returns star'''
        return parsers.get_star(self.__chebi_id)

    def get_database_accessions(self):
        '''Returns database accessions'''
        return parsers.get_all_database_accessions(self.__get_all_ids())

    def get_inchi(self):
        '''Returns inchi'''
        inchi = parsers.get_inchi(self.__chebi_id)

        if inchi is None:
            inchi = parsers.get_inchi(self.get_parent_id())

        if inchi is None:
            for parent_or_child_id in self.__get_all_ids():
                inchi = parsers.get_inchi(parent_or_child_id)

                if inchi is not None:
                    break

        return inchi

    def get_inchi_key(self):
        '''Returns inchi key'''
        structure = parsers.get_inchi_key(self.__chebi_id)

        if structure is None:
            structure = parsers.get_inchi_key(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self.__get_all_ids():
                structure = parsers.get_inchi_key(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_smiles(self):
        '''Returns smiles'''
        structure = parsers.get_smiles(self.__chebi_id)

        if structure is None:
            structure = parsers.get_smiles(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self.__get_all_ids():
                structure = parsers.get_smiles(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_mol(self):
        '''Returns mol'''
        structure = parsers.get_mol(self.__chebi_id)

        if structure is None:
            structure = parsers.get_mol(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self.__get_all_ids():
                structure = parsers.get_mol(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_mol_filename(self):
        '''Returns mol filename'''
        mol_filename = parsers.get_mol_filename(self.__chebi_id)

        if mol_filename is None:
            mol_filename = parsers.get_mol_filename(self.get_parent_id())

        if mol_filename is None:
            for parent_or_child_id in self.__get_all_ids():
                mol_filename = \
                    parsers.get_mol_filename(parent_or_child_id)

                if mol_filename is not None:
                    break

        return mol_filename

    def get_names(self):
        '''Returns names'''
        return parsers.get_all_names(self.__get_all_ids())

    def get_references(self):
        '''Returns references'''
        return parsers.get_references(self.__get_all_ids())

    def get_compound_origins(self):
        '''Returns compound origins'''
        return parsers.get_all_compound_origins(self.__get_all_ids())

    def get_outgoings(self):
        '''Returns outgoings'''
        return parsers.get_all_outgoings(self.__get_all_ids())

    def get_incomings(self):
        '''Returns incomings'''
        return parsers.get_all_incomings(self.__get_all_ids())

    def __get_status(self):
        '''Returns status'''
        return parsers.get_status(self.__chebi_id)

    def __get_all_ids(self):
        '''Returns all ids'''
        if self.__all_ids is None:
            parent_id = self.get_parent_id()
            self.__all_ids = parsers.get_all_ids(self.__chebi_id
                                                 if math.isnan(parent_id)
                                                 else parent_id)

            if self.__all_ids is None:
                self.__all_ids = []

        return self.__all_ids


def main():
    '''Example code, showing the instantiation of a ChebiEntity, a call to
    get_name(), get_outgoings() and the calling of a number of methods of the
    returned Relation objects.'''
    chebi_entity = ChebiEntity(15903)

    print chebi_entity.get_name()

    for outgoing in chebi_entity.get_outgoings():
        target_chebi_entity = ChebiEntity(outgoing.get_target_chebi_id())
        print outgoing.get_type() + '\t' + target_chebi_entity.get_name()

if __name__ == '__main__':
    main()
