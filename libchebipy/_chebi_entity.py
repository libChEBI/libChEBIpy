'''
libChEBIpy (c) University of Manchester 2015-2020

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=superfluous-parens
# pylint: disable=too-many-public-methods
import math
import sys

from ._base_object import BaseObject


class ChebiException(Exception):
    '''COMMENT'''
    pass


class ChebiEntity(BaseObject):
    '''Class representing a single entity in the ChEBI database.'''

    def __init__(self, chebi_id, parser="filesystem", auto_update=True, download_dir=None):
        self.__chebi_id = int(chebi_id.replace('CHEBI:', ''))
        self.__all_ids = None
        self._get_parser(parser, download_dir, auto_update)

        if self.get_name() is None:
            raise ChebiException('ChEBI id ' + chebi_id + ' invalid')

    def _get_parser(self, parser_name, download_dir, auto_update):
        parser_name = parser_name.lower().replace('-', '')
        if parser_name not in ["filesystem", "googlestorage"]:
            raise ChebiException('Parser %s is not valid.' % parser_name)
        
        # Save to filesystem cache
        if parser_name == "filesystem":
            from ._parsers.filesystem import FileSystemCache
            self.parser = FileSystemCache(download_dir=download_dir, auto_update=auto_update)

        # Save to Google storage cache
        elif parser_name == "googlestorage":
            from ._parsers.googlestorage import GoogleStorageCache
            self.parser = GoogleStorageCache(download_dir=download_dir, auto_update=auto_update)

    def get_id(self):
        '''Returns id'''
        return 'CHEBI:' + str(self.__chebi_id)

    def get_parent_id(self):
        '''Returns parent id'''
        parent_id = self.parser.get_parent_id(self.__chebi_id)
        return None if math.isnan(parent_id) else 'CHEBI:' + str(parent_id)

    def get_formulae(self):
        '''Returns formulae'''
        return self.parser.get_all_formulae(self.__get_all_ids())

    def get_formula(self):
        '''Returns formula'''
        formulae = self.get_formulae()
        return None if len(formulae) == 0 else formulae[0].get_formula()

    def get_mass(self):
        '''Returns mass'''
        mass = self.parser.get_mass(self.__chebi_id)

        if math.isnan(mass):
            mass = self.parser.get_mass(self.get_parent_id())

        if math.isnan(mass):
            for parent_or_child_id in self.__get_all_ids():
                mass = self.parser.get_mass(parent_or_child_id)

                if not math.isnan(mass):
                    break

        return mass

    def get_charge(self):
        '''Returns charge'''
        charge = self.parser.get_charge(self.__chebi_id)

        if math.isnan(charge):
            charge = self.parser.get_charge(self.get_parent_id())

        if math.isnan(charge):
            for parent_or_child_id in self.__get_all_ids():
                charge = self.parser.get_charge(parent_or_child_id)

                if not math.isnan(charge):
                    break

        return charge

    def get_comments(self):
        '''Returns comments'''
        return self.parser.get_all_comments(self.__get_all_ids())

    def get_source(self):
        '''Returns source'''
        return self.parser.get_source(self.__chebi_id)

    def get_name(self):
        '''Returns name'''
        name = self.parser.get_name(self.__chebi_id)

        if name is None:
            name = self.parser.get_name(self.get_parent_id())

        if name is None:
            for parent_or_child_id in self.__get_all_ids():
                name = self.parser.get_name(parent_or_child_id)

                if name is not None:
                    break

        return name

    def get_definition(self):
        '''Returns definition'''
        definition = self.parser.get_definition(self.__chebi_id)

        if definition is None:
            definition = self.parser.get_definition(self.get_parent_id())

        if definition is None:
            for parent_or_child_id in self.__get_all_ids():
                definition = self.parser.get_definition(parent_or_child_id)

                if definition is not None:
                    break

        return definition

    def get_modified_on(self):
        '''Returns modified on'''
        return self.parser.get_all_modified_on(self.__get_all_ids())

    def get_created_by(self):
        '''Returns created by'''
        created_by = self.parser.get_created_by(self.__chebi_id)

        if created_by is None:
            created_by = self.parser.get_created_by(self.get_parent_id())

        if created_by is None:
            for parent_or_child_id in self.__get_all_ids():
                created_by = self.parser.get_created_by(parent_or_child_id)

                if created_by is not None:
                    break

        return created_by

    def get_star(self):
        '''Returns star'''
        return self.parser.get_star(self.__chebi_id)

    def get_database_accessions(self):
        '''Returns database accessions'''
        return self.parser.get_all_database_accessions(self.__get_all_ids())

    def get_inchi(self):
        '''Returns inchi'''
        inchi = self.parser.get_inchi(self.__chebi_id)

        if inchi is None:
            inchi = self.parser.get_inchi(self.get_parent_id())

        if inchi is None:
            for parent_or_child_id in self.__get_all_ids():
                inchi = self.parser.get_inchi(parent_or_child_id)

                if inchi is not None:
                    break

        return inchi

    def get_inchi_key(self):
        '''Returns inchi key'''
        structure = self.parser.get_inchi_key(self.__chebi_id)

        if structure is None:
            structure = self.parser.get_inchi_key(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self.__get_all_ids():
                structure = self.parser.get_inchi_key(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_smiles(self):
        '''Returns smiles'''
        structure = self.parser.get_smiles(self.__chebi_id)

        if structure is None:
            structure = self.parser.get_smiles(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self.__get_all_ids():
                structure = self.parser.get_smiles(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_mol(self):
        '''Returns mol'''
        structure = self.parser.get_mol(self.__chebi_id)

        if structure is None:
            structure = self.parser.get_mol(self.get_parent_id())

        if structure is None:
            for parent_or_child_id in self.__get_all_ids():
                structure = self.parser.get_mol(parent_or_child_id)

                if structure is not None:
                    break

        return None if structure is None else structure.get_structure()

    def get_mol_filename(self):
        '''Returns mol filename'''
        mol_filename = self.parser.get_mol_filename(self.__chebi_id)

        if mol_filename is None:
            mol_filename = self.parser.get_mol_filename(self.get_parent_id())

        if mol_filename is None:
            for parent_or_child_id in self.__get_all_ids():
                mol_filename = \
                    self.parser.get_mol_filename(parent_or_child_id)

                if mol_filename is not None:
                    break

        return mol_filename

    def get_names(self):
        '''Returns names'''
        return self.parser.get_all_names(self.__get_all_ids())

    def get_references(self):
        '''Returns references'''
        return self.parser.get_references(self.__get_all_ids())

    def get_compound_origins(self):
        '''Returns compound origins'''
        return self.parser.get_all_compound_origins(self.__get_all_ids())

    def get_outgoings(self):
        '''Returns outgoings'''
        return self.parser.get_all_outgoings(self.__get_all_ids())

    def get_incomings(self):
        '''Returns incomings'''
        return self.parser.get_all_incomings(self.__get_all_ids())

    def __get_status(self):
        '''Returns status'''
        return self.parser.get_status(self.__chebi_id)

    def __get_all_ids(self):
        '''Returns all ids'''
        if self.__all_ids is None:
            parent_id = self.parser.get_parent_id(self.__chebi_id)
            self.__all_ids = self.parser.get_all_ids(self.__chebi_id
                                                 if math.isnan(parent_id)
                                                 else parent_id)

            if self.__all_ids is None:
                self.__all_ids = []

        return self.__all_ids


def main(parser_name="filesystem"):
    '''Example code, showing the instantiation of a ChebiEntity, a call to
        get_name(), get_outgoings() and the calling of a number of methods of the
        returned Relation objects.
    '''
    chebi_entity = ChebiEntity(15903, parser=parser_name)

    print(chebi_entity.get_name())

    for outgoing in chebi_entity.get_outgoings():
        target_chebi_entity = ChebiEntity(outgoing.get_target_chebi_id())
        print(outgoing.get_type() + '\t' + target_chebi_entity.get_name())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    main(parser_name)
