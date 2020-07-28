'''
libChEBIpy (c) University of Manchester 2015-2020

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import datetime
import gzip
import io
import os.path
import re
import tempfile
import zipfile

import six.moves.urllib.parse as urlparse
from six.moves.urllib.request import urlretrieve, urlcleanup

from .._comment import Comment
from .._compound_origin import CompoundOrigin
from .._database_accession import DatabaseAccession
from .._formula import Formula
from .._name import Name
from .._reference import Reference
from .._relation import Relation
from .._structure import Structure

from .base import ParserBase


class FileSystemCache(ParserBase):
    """A filesystem cache saves files on the user's local filesystem for later 
       use. The functions defined here are any from the original Parser Base
       that would warrant opening a file on the filesystem.
    """
    def __init__(self, download_dir=None, auto_update=True):
        super().__init__(download_dir, auto_update)

    def _parse_chemical_data(self):
        '''Gets and parses file using the local filesystem'''
        filename = get_file('chemical_data.tsv')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')

                if tokens[3] == 'FORMULA':
                    # Many seemingly contradictory formulae exist,
                    # depending upon the source database
                    chebi_id = int(tokens[1])

                    if chebi_id not in self._FORMULAE:
                        self._FORMULAE[chebi_id] = []

                    # Append formula:
                    form = Formula(tokens[4], tokens[2])
                    self._FORMULAE[chebi_id].append(form)

                elif tokens[3] == 'MASS':
                    self._MASSES[int(tokens[1])] = float(tokens[4])

                elif tokens[3] == 'CHARGE':
                    self._CHARGES[int(tokens[1])] = int(tokens[4]
                                                    if tokens[4][-1] != '-'
                                                    else '-' + tokens[4][:-1])


    def _parse_comments(self):
        '''Gets and parses file'''
        filename = get_file('comments.tsv')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')
                chebi_id = int(tokens[1])

                if chebi_id not in self._COMMENTS:
                    self._COMMENTS[chebi_id] = []

                # Append Comment:
                com = Comment(tokens[3],
                              tokens[4],
                              tokens[5],
                              datetime.datetime.strptime(tokens[2], '%Y-%M-%d'))

                self._COMMENTS[chebi_id].append(com)


    def _parse_compound_origins(self):
        '''Gets and parses file'''
        filename = get_file('compound_origins.tsv')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')

                if len(tokens) > 10:
                    chebi_id = int(tokens[1])

                    if chebi_id not in self._COMPOUND_ORIGINS:
                        self._COMPOUND_ORIGINS[chebi_id] = []

                    # Append CompoundOrigin:
                    comp_orig = CompoundOrigin(tokens[2], tokens[3],
                                               tokens[4], tokens[5],
                                               tokens[6], tokens[7],
                                               tokens[8], tokens[9],
                                               tokens[10])
                    self._COMPOUND_ORIGINS[chebi_id].append(comp_orig)


    def _parse_compounds(self):
        '''Gets and parses file'''
        filename = get_file('compounds.tsv.gz')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')
                chebi_id = int(tokens[0])
    
                self._STATUSES[chebi_id] = tokens[1]
                self._SOURCES[chebi_id] = tokens[3]

                parent_id_token = tokens[4]
                self._PARENT_IDS[chebi_id] = float('NaN') \
                    if parent_id_token == 'null' \
                    else int(parent_id_token)
                self._put_all_ids(chebi_id, chebi_id)

                if parent_id_token != 'null':
                    parent_id = int(parent_id_token)
                    self._put_all_ids(parent_id, chebi_id)

                self._NAMES[chebi_id] = None if tokens[5] == 'null' else tokens[5]
                self._DEFINITIONS[chebi_id] = None if tokens[6] == 'null' \
                    else tokens[6]
                self._MODIFIED_ONS[chebi_id] = None if tokens[7] == 'null' \
                    else datetime.datetime.strptime(tokens[7], '%Y-%m-%d')
                self._CREATED_BYS[chebi_id] = None if tokens[8] == 'null' \
                    or len(tokens) == 9 else tokens[8]
                self._STARS[chebi_id] = float('NaN') \
                    if tokens[9 if len(tokens) > 9 else 8] == 'null' \
                    else int(tokens[9 if len(tokens) > 9 else 8])


    def _parse_database_accessions(self):
        '''Gets and parses file'''
        filename = get_file('database_accession.tsv')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')
                chebi_id = int(tokens[1])

                if chebi_id not in self._DATABASE_ACCESSIONS:
                    self._DATABASE_ACCESSIONS[chebi_id] = []

                # Append DatabaseAccession:
                dat_acc = DatabaseAccession(tokens[3], tokens[4], tokens[2])
                self._DATABASE_ACCESSIONS[chebi_id].append(dat_acc)


    def _parse_inchi(self):
        '''Gets and parses file'''
        filename = get_file('chebiId_inchi.tsv')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')
                self._INCHIS[int(tokens[0])] = tokens[1]


    def _parse_names(self):
        '''Gets and parses file'''
        filename = get_file('names.tsv.gz')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')
                chebi_id = int(tokens[1])

                if chebi_id not in self._ALL_NAMES:
                    self._ALL_NAMES[chebi_id] = []

                # Append Name:
                nme = Name(tokens[4],
                           tokens[2],
                           tokens[3],
                           tokens[5] == 'T',
                           tokens[6])

                self._ALL_NAMES[chebi_id].append(nme)

    def get_references(self, chebi_ids):
        '''Returns references'''
        references = []
        chebi_ids = [str(chebi_id) for chebi_id in chebi_ids]

        filename = get_file('reference.tsv.gz')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split('\t')

                if tokens[0] in chebi_ids:
                    # Append Reference:
                    if len(tokens) > 3:
                        ref = Reference(tokens[1], tokens[2], tokens[3],
                                        tokens[4])
                    else:
                        ref = Reference(tokens[1], tokens[2])

                    references.append(ref)
        return references


    def _parse_relation(self):
        '''Gets and parses file'''
        relation_filename = get_file('relation.tsv')
        relation_textfile = open(relation_filename, 'r')

        next(relation_textfile)

        for line in relation_textfile:
            tokens = line.strip().split('\t')

            source_chebi_id = int(tokens[3])
            target_chebi_id = int(tokens[2])
            typ = tokens[1]

            if source_chebi_id not in self._OUTGOINGS:
                self._OUTGOINGS[source_chebi_id] = []

            if target_chebi_id not in self._INCOMINGS:
                self._INCOMINGS[target_chebi_id] = []

            target_relation = Relation(typ, str(target_chebi_id), tokens[4])
            source_relation = Relation(typ, str(source_chebi_id), tokens[4])

            self._OUTGOINGS[source_chebi_id].append(target_relation)
            self._INCOMINGS[target_chebi_id].append(source_relation)



    def get_mol(self, chebi_id):
        '''Returns mol'''
        chebi_id_regexp = '^\\d+\\,' + str(chebi_id) + '\\,.*'
        mol_file_end_regexp = '\",mol,\\dD,[Y\\|N],[Y\\|N]$'
        this_structure = []

        filename = get_file('structures.csv.gz')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            in_chebi_id = False

            next(textfile)

            for line in textfile:
                if in_chebi_id or line[0].isdigit():
                    if re.match(chebi_id_regexp, line):
                        tokens = line.strip().split(',')
                        in_chebi_id = True
                        this_structure = []
                        this_structure.append(','.join(tokens[2:])
                                              .replace('\"', ''))
                        this_structure.append('\n')
                    elif in_chebi_id:

                        if re.match(mol_file_end_regexp, line):
                            tokens = line.strip().split(',')

                            if _is_default_structure(tokens[3]):
                                tokens = line.strip().split(',')
                                this_structure.append(tokens[0].replace('\"', ''))
                                return Structure(''.join(this_structure),
                                                 Structure.mol,
                                                 int(tokens[2][0]))

                            # else:
                            this_structure = []
                            in_chebi_id = False
                            continue

                        this_structure.append(line)


    def get_mol_filename(self, chebi_id):
        '''Returns mol file'''
        mol = get_mol(chebi_id)

        if mol is None:
            return None

        file_descriptor, mol_filename = tempfile.mkstemp(str(chebi_id) +
                                                     '_', '.mol')
        with open(mol_filename, 'w') as mol_file:
            mol_file.write(mol.get_structure())
        os.close(file_descriptor)
        return mol_filename


    def _parse_structures(self):
        '''COMMENT'''
        filename = get_file('structures.csv.gz')

        with io.open(filename, 'r', encoding='cp1252') as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split(',')

                if len(tokens) == 7:
                    if tokens[3] == 'InChIKey':
                        self._INCHI_KEYS[int(tokens[1])] = \
                            Structure(tokens[2],
                                      Structure.InChIKey,
                                      int(tokens[4][0]))
                    elif tokens[3] == 'SMILES':
                        self._SMILES[int(tokens[1])] = \
                            Structure(tokens[2],
                                      Structure.SMILES,
                                      int(tokens[4][0]))


    def get_file(self, filename):
        '''Downloads filename from ChEBI FTP site'''
        destination = __DOWNLOAD_PARAMS['path']
        filepath = os.path.join(destination, filename)

        if not __is_current(filepath):

            if not os.path.exists(destination):
                os.makedirs(destination)

            url = 'ftp://ftp.ebi.ac.uk/pub/databases/chebi/' + \
                'Flat_file_tab_delimited/'
            urlretrieve(urlparse.urljoin(url, filename), filepath)
            urlcleanup()

        if filepath.endswith('.zip'):
            zfile = zipfile.ZipFile(filepath, 'r')
            filepath = os.path.join(destination, zfile.namelist()[0])
            zfile.extractall(destination)

        elif filepath.endswith('.gz'):
            unzipped_filepath = filepath[:-len('.gz')]
            if os.path.exists(unzipped_filepath) \
                    and self._is_current(unzipped_filepath):
                filepath = unzipped_filepath
            else:
                input_file = gzip.open(filepath, 'rb')
                filepath = os.path.join(destination, input_file.name[:-len('.gz')])
                output_file = open(filepath, 'wb')

                for line in input_file:
                    output_file.write(line)

                input_file.close()
                output_file.close()

        return filepath


    def _is_current(self, filepath):
        '''Checks whether file is current'''
        if not __DOWNLOAD_PARAMS['auto_update']:
            return True

        if not os.path.isfile(filepath):
            return False

        return datetime.datetime.utcfromtimestamp(os.path.getmtime(filepath)) \
            > __get_last_update_time()
