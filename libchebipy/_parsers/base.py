"""
libChEBIpy (c) University of Manchester 2015-2020

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
"""

import calendar
import datetime
import gzip
import io
import os.path
import re
import zipfile
import tempfile

from .._comment import Comment
from .._compound_origin import CompoundOrigin
from .._database_accession import DatabaseAccession
from .._formula import Formula
from .._name import Name
from .._reference import Reference
from .._relation import Relation
from .._structure import Structure


class ParserBase:
    """A parser base provides shared functions to interact with a libchebi cache
    """

    def __init__(self, download_dir=None, auto_update=True):
        """set a unique id that includes executor name (type) and random uuid)
        """
        # First preference to command line, then environment, then default
        self.download_dir = download_dir or os.environ.get(
            "LIBCHEBIPY_DOWNLOAD_DIR", os.path.join(os.path.expanduser("~"), "libChEBI")
        )
        self.path = self.download_dir
        self.auto_update = auto_update

        self._ALL_IDS = {}
        self._ALL_NAMES = {}
        self._COMMENTS = {}
        self._COMPOUND_ORIGINS = {}
        self._CHARGES = {}
        self._CREATED_BYS = {}
        self._DATABASE_ACCESSIONS = {}
        self._DEFAULT_STRUCTURE_IDS = []
        self._DEFINITIONS = {}
        self._FORMULAE = {}
        self._INCHIS = {}
        self._INCHI_KEYS = {}
        self._INCOMINGS = {}
        self._MASSES = {}
        self._MODIFIED_ONS = {}
        self._NAMES = {}
        self._OUTGOINGS = {}
        self._PARENT_IDS = {}
        self._SMILES = {}
        self._SOURCES = {}
        self._STARS = {}
        self._STATUSES = {}

    def set_download_cache_path(self, path):
        """Sets download cache path."""
        self.path = path

    def set_auto_update(self, auto_update):
        """Sets auto update flag."""
        self.auto_update = auto_update

    def get_formulae(self, chebi_id):
        """Returns formulae"""
        if not self._FORMULAE:
            self._parse_chemical_data()
        return self._FORMULAE[chebi_id] if chebi_id in self._FORMULAE else []

    def get_all_formulae(self, chebi_ids):
        """Returns all formulae"""
        all_formulae = [self.get_formulae(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_formulae for x in sublist]

    def get_mass(self, chebi_id):
        """Returns mass"""
        if not self._MASSES:
            self._parse_chemical_data()
        return self._MASSES[chebi_id] if chebi_id in self._MASSES else float("NaN")

    def get_charge(self, chebi_id):
        """Returns charge"""
        if not self._CHARGES:
            self._parse_chemical_data()
        return self._CHARGES[chebi_id] if chebi_id in self._CHARGES else float("NaN")

    def get_comments(self, chebi_id):
        """Returns comments"""
        if not self._COMMENTS:
            self._parse_comments()
        return self._COMMENTS[chebi_id] if chebi_id in self._COMMENTS else []

    def get_all_comments(self, chebi_ids):
        """Returns all comments"""
        all_comments = [self.get_comments(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_comments for x in sublist]

    def get_compound_origins(self, chebi_id):
        """Returns compound origins"""
        if not self._COMPOUND_ORIGINS:
            self._parse_compound_origins()
        return (
            self._COMPOUND_ORIGINS[chebi_id]
            if chebi_id in self._COMPOUND_ORIGINS
            else []
        )

    def get_all_compound_origins(self, chebi_ids):
        """Returns all compound origins"""
        all_compound_origins = [
            self.get_compound_origins(chebi_id) for chebi_id in chebi_ids
        ]
        return [x for sublist in all_compound_origins for x in sublist]

    def get_status(self, chebi_id):
        """Returns status"""
        if not self._STATUSES:
            self._parse_compounds()
        return self._STATUSES[chebi_id] if chebi_id in self._STATUSES else None

    def get_source(self, chebi_id):
        """Returns source"""
        if not self._SOURCES:
            self._parse_compounds()
        return self._SOURCES[chebi_id] if chebi_id in self._SOURCES else None

    def get_parent_id(self, chebi_id):
        """Returns parent id"""
        if not self._PARENT_IDS:
            self._parse_compounds()
        return (
            self._PARENT_IDS[chebi_id] if chebi_id in self._PARENT_IDS else float("NaN")
        )

    def get_all_ids(self, chebi_id):
        """Returns all ids"""
        if not self._ALL_IDS:
            self._parse_compounds()
        return self._ALL_IDS[chebi_id] if chebi_id in self._ALL_IDS else []

    def get_name(self, chebi_id):
        """Returns name"""
        if not self._NAMES:
            self._parse_compounds()
        return self._NAMES[chebi_id] if chebi_id in self._NAMES else None

    def get_definition(self, chebi_id):
        """Returns definition"""
        if not self._DEFINITIONS:
            self._parse_compounds()
        return self._DEFINITIONS[chebi_id] if chebi_id in self._DEFINITIONS else None

    def get_modified_on(self, chebi_id):
        """Returns modified on"""
        if not self._MODIFIED_ONS:
            self._parse_compounds()
        return self._MODIFIED_ONS[chebi_id] if chebi_id in self._MODIFIED_ONS else None

    def get_all_modified_on(self, chebi_ids):
        """Returns all modified on"""
        all_modified_ons = [self.get_modified_on(chebi_id) for chebi_id in chebi_ids]
        all_modified_ons = [
            modified_on for modified_on in all_modified_ons if modified_on is not None
        ]
        return None if not all_modified_ons else sorted(all_modified_ons)[-1]

    def get_created_by(self, chebi_id):
        """Returns created by"""
        if not self._CREATED_BYS:
            self._parse_compounds()
        return self._CREATED_BYS[chebi_id] if chebi_id in self._MODIFIED_ONS else None

    def get_star(self, chebi_id):
        """Returns star"""
        if not self._STARS:
            self._parse_compounds()
        return self._STARS[chebi_id] if chebi_id in self._STARS else float("NaN")

    def _put_all_ids(self, parent_id, child_id):
        """Add a parent and child id to the list of all ids"""
        if parent_id in self._ALL_IDS:
            self._ALL_IDS[parent_id].append(child_id)
        else:
            self._ALL_IDS[parent_id] = [child_id]

    def get_database_accessions(self, chebi_id):
        """Returns database accession"""
        if not self._DATABASE_ACCESSIONS:
            self._parse_database_accessions()

        return (
            self._DATABASE_ACCESSIONS[chebi_id]
            if chebi_id in self._DATABASE_ACCESSIONS
            else []
        )

    def get_all_database_accessions(self, chebi_ids):
        """Returns all database accessions"""
        all_database_accessions = [
            self.get_database_accessions(chebi_id) for chebi_id in chebi_ids
        ]
        return [x for sublist in all_database_accessions for x in sublist]

    def get_inchi(self, chebi_id):
        """Returns InChI string"""
        if not self._INCHIS:
            self._parse_inchi()
        return self._INCHIS[chebi_id] if chebi_id in self._INCHIS else None

    def get_names(self, chebi_id):
        """Returns names"""
        if not self._ALL_NAMES:
            self._parse_names()
        return self._ALL_NAMES[chebi_id] if chebi_id in self._ALL_NAMES else []

    def get_all_names(self, chebi_ids):
        """Returns all names"""
        all_names = [self.get_names(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_names for x in sublist]

    def get_outgoings(self, chebi_id):
        """Returns outgoings"""
        if not self._OUTGOINGS:
            self._parse_relation()
        return self._OUTGOINGS[chebi_id] if chebi_id in self._OUTGOINGS else []

    def get_all_outgoings(self, chebi_ids):
        """Returns all outgoings"""
        all_outgoings = [self.get_outgoings(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_outgoings for x in sublist]

    def get_incomings(self, chebi_id):
        """Returns incomings"""
        if not self._INCOMINGS:
            self._parse_relation()
        return self._INCOMINGS[chebi_id] if chebi_id in self._INCOMINGS else []

    def get_all_incomings(self, chebi_ids):
        """Returns all incomings"""
        all_incomings = [self.get_incomings(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_incomings for x in sublist]

    def get_inchi_key(self, chebi_id):
        """Returns InChI key"""
        if not self._INCHI_KEYS:
            self._parse_structures()
        return self._INCHI_KEYS[chebi_id] if chebi_id in self._INCHI_KEYS else None

    def get_smiles(self, chebi_id):
        """Returns InChI key"""
        if not self._SMILES:
            self._parse_structures()
        return self._SMILES[chebi_id] if chebi_id in self._SMILES else None

    def _get_last_update_time(self):
        """Returns last FTP site update time"""
        now = datetime.datetime.utcnow()

        # Get the first Tuesday of the month
        first_tuesday = self._get_first_tuesday(now)

        if first_tuesday < now:
            return first_tuesday

        first_of_month = datetime.datetime(now.year, now.month, 1)
        last_month = first_of_month + datetime.timedelta(days=-1)
        return self._get_first_tuesday(last_month)

    def _get_first_tuesday(self, this_date):
        """Get the first Tuesday of the month"""
        month_range = calendar.monthrange(this_date.year, this_date.month)
        first_of_month = datetime.datetime(this_date.year, this_date.month, 1)
        first_tuesday_day = (calendar.TUESDAY - month_range[0]) % 7
        first_tuesday = first_of_month + datetime.timedelta(days=first_tuesday_day)
        return first_tuesday

    def _extract_compressed_file(self, filepath, destination):
        """If a filename is compressed, extract the contents. If not,
           return path as is
        """
        if filepath.endswith(".zip"):
            zfile = zipfile.ZipFile(filepath, "r")
            filepath = os.path.join(destination, zfile.namelist()[0])
            zfile.extractall(destination)

        elif filepath.endswith(".gz"):
            unzipped_filepath = filepath[: -len(".gz")]
            if os.path.exists(unzipped_filepath) and self._is_current(
                unzipped_filepath
            ):
                filepath = unzipped_filepath
            else:
                input_file = gzip.open(filepath, "rb")
                filepath = os.path.join(destination, input_file.name[: -len(".gz")])
                output_file = open(filepath, "wb")

                for line in input_file:
                    output_file.write(line)

                input_file.close()
                output_file.close()

        return filepath

    def _is_default_structure(self, def_struct):
        """Is default structure?"""
        return def_struct.upper() == "Y"

    def _parse_chemical_data(self):
        """Gets and parses file using the local filesystem"""
        filename = self.get_file("chemical_data.tsv")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")

                if tokens[3] == "FORMULA":
                    # Many seemingly contradictory formulae exist,
                    # depending upon the source database
                    chebi_id = int(tokens[1])

                    if chebi_id not in self._FORMULAE:
                        self._FORMULAE[chebi_id] = []

                    # Append formula:
                    form = Formula(tokens[4], tokens[2])
                    self._FORMULAE[chebi_id].append(form)

                elif tokens[3] == "MASS":
                    self._MASSES[int(tokens[1])] = float(tokens[4])

                elif tokens[3] == "CHARGE":
                    self._CHARGES[int(tokens[1])] = int(
                        tokens[4] if tokens[4][-1] != "-" else "-" + tokens[4][:-1]
                    )

    def _parse_comments(self):
        """Gets and parses file"""

        filename = self.get_file("comments.tsv")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")
                chebi_id = int(tokens[1])

                if chebi_id not in self._COMMENTS:
                    self._COMMENTS[chebi_id] = []

                # Append Comment:
                com = Comment(
                    tokens[3],
                    tokens[4],
                    tokens[5],
                    datetime.datetime.strptime(tokens[2], "%Y-%M-%d"),
                )

                self._COMMENTS[chebi_id].append(com)

    def _parse_compound_origins(self):
        """Gets and parses file"""
        filename = self.get_file("compound_origins.tsv")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")

                if len(tokens) > 10:
                    chebi_id = int(tokens[1])

                    if chebi_id not in self._COMPOUND_ORIGINS:
                        self._COMPOUND_ORIGINS[chebi_id] = []

                    # Append CompoundOrigin:
                    comp_orig = CompoundOrigin(
                        tokens[2],
                        tokens[3],
                        tokens[4],
                        tokens[5],
                        tokens[6],
                        tokens[7],
                        tokens[8],
                        tokens[9],
                        tokens[10],
                    )
                    self._COMPOUND_ORIGINS[chebi_id].append(comp_orig)

    def _parse_compounds(self):
        """Gets and parses file"""

        filename = self.get_file("compounds.tsv.gz")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")
                chebi_id = int(tokens[0])

                self._STATUSES[chebi_id] = tokens[1]
                self._SOURCES[chebi_id] = tokens[3]

                parent_id_token = tokens[4]
                self._PARENT_IDS[chebi_id] = (
                    float("NaN") if parent_id_token == "null" else int(parent_id_token)
                )
                self._put_all_ids(chebi_id, chebi_id)

                if parent_id_token != "null":
                    parent_id = int(parent_id_token)
                    self._put_all_ids(parent_id, chebi_id)

                self._NAMES[chebi_id] = None if tokens[5] == "null" else tokens[5]
                self._DEFINITIONS[chebi_id] = None if tokens[6] == "null" else tokens[6]
                self._MODIFIED_ONS[chebi_id] = (
                    None
                    if tokens[7] == "null"
                    else datetime.datetime.strptime(tokens[7], "%Y-%m-%d")
                )
                self._CREATED_BYS[chebi_id] = (
                    None if tokens[8] == "null" or len(tokens) == 9 else tokens[8]
                )
                self._STARS[chebi_id] = (
                    float("NaN")
                    if tokens[9 if len(tokens) > 9 else 8] == "null"
                    else int(tokens[9 if len(tokens) > 9 else 8])
                )

    def _parse_database_accessions(self):
        """Gets and parses file"""

        filename = self.get_file("database_accession.tsv")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")
                chebi_id = int(tokens[1])

                if chebi_id not in self._DATABASE_ACCESSIONS:
                    self._DATABASE_ACCESSIONS[chebi_id] = []

                # Append DatabaseAccession:
                dat_acc = DatabaseAccession(tokens[3], tokens[4], tokens[2])
                self._DATABASE_ACCESSIONS[chebi_id].append(dat_acc)

    def _parse_inchi(self):
        """Gets and parses file"""

        filename = self.get_file("chebiId_inchi.tsv")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")
                self._INCHIS[int(tokens[0])] = tokens[1]

    def _parse_names(self):
        """Gets and parses file"""

        filename = self.get_file("names.tsv.gz")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")
                chebi_id = int(tokens[1])

                if chebi_id not in self._ALL_NAMES:
                    self._ALL_NAMES[chebi_id] = []

                # Append Name:
                nme = Name(tokens[4], tokens[2], tokens[3], tokens[5] == "T", tokens[6])

                self._ALL_NAMES[chebi_id].append(nme)

    def get_references(self, chebi_ids):
        """Returns references"""

        references = []
        chebi_ids = [str(chebi_id) for chebi_id in chebi_ids]

        filename = self.get_file("reference.tsv.gz")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split("\t")

                if tokens[0] in chebi_ids:
                    # Append Reference:
                    if len(tokens) > 3:
                        ref = Reference(tokens[1], tokens[2], tokens[3], tokens[4])
                    else:
                        ref = Reference(tokens[1], tokens[2])

                    references.append(ref)
        return references

    def _parse_relation(self):
        """Gets and parses file"""

        relation_filename = self.get_file("relation.tsv")
        relation_textfile = open(relation_filename, "r")

        next(relation_textfile)

        for line in relation_textfile:
            tokens = line.strip().split("\t")

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
        """Returns mol"""

        chebi_id_regexp = "^\\d+\\," + str(chebi_id) + "\\,.*"
        mol_file_end_regexp = '",mol,\\dD,[Y\\|N],[Y\\|N]$'
        this_structure = []

        filename = self.get_file("structures.csv.gz")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            in_chebi_id = False

            next(textfile)

            for line in textfile:
                if in_chebi_id or line[0].isdigit():
                    if re.match(chebi_id_regexp, line):
                        tokens = line.strip().split(",")
                        in_chebi_id = True
                        this_structure = []
                        this_structure.append(",".join(tokens[2:]).replace('"', ""))
                        this_structure.append("\n")
                    elif in_chebi_id:

                        if re.match(mol_file_end_regexp, line):
                            tokens = line.strip().split(",")

                            if self._is_default_structure(tokens[3]):
                                tokens = line.strip().split(",")
                                this_structure.append(tokens[0].replace('"', ""))
                                return Structure(
                                    "".join(this_structure),
                                    Structure.mol,
                                    int(tokens[2][0]),
                                )

                            # else:
                            this_structure = []
                            in_chebi_id = False
                            continue

                        this_structure.append(line)

    def get_mol_filename(self, chebi_id):
        """Returns mol file"""
        mol = self.get_mol(chebi_id)

        if mol is None:
            return None

        file_descriptor, mol_filename = tempfile.mkstemp(str(chebi_id) + "_", ".mol")
        with open(mol_filename, "w") as mol_file:
            mol_file.write(mol.get_structure())
        os.close(file_descriptor)
        return mol_filename

    def _parse_structures(self):
        """COMMENT"""
        filename = self.get_file("structures.csv.gz")

        with io.open(filename, "r", encoding="cp1252") as textfile:
            next(textfile)

            for line in textfile:
                tokens = line.strip().split(",")

                if len(tokens) == 7:
                    if tokens[3] == "InChIKey":
                        self._INCHI_KEYS[int(tokens[1])] = Structure(
                            tokens[2], Structure.InChIKey, int(tokens[4][0])
                        )
                    elif tokens[3] == "SMILES":
                        self._SMILES[int(tokens[1])] = Structure(
                            tokens[2], Structure.SMILES, int(tokens[4][0])
                        )
