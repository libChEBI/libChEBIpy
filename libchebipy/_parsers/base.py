'''
libChEBIpy (c) University of Manchester 2015-2020

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''

import calendar
import datetime
import os.path


class ParserBase:
    """A parser base provides shared functions to interact with a libchebi cache
    """
    def __init__(self, download_dir=None, auto_update=True):
        """set a unique id that includes executor name (type) and random uuid)
        """
        # First preference to command line, then environment, then default
        self.download_dir = download_dir or os.environ.get('LIBCHEBIPY_DOWNLOAD_DIR', os.path.join(os.path.expanduser('~'), 'libChEBI'))
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

    # Public functions

    def set_download_cache_path(self, path):
        '''Sets download cache path.'''
        self.path = path

    def set_auto_update(auto_update):
        '''Sets auto update flag.'''
        self.auto_update = auto_update

    def get_formulae(self, chebi_id):
        '''Returns formulae'''
        if not self._FORMULAE:
            self._parse_chemical_data()
        return self._FORMULAE[chebi_id] if chebi_id in self._FORMULAE else []


    def get_all_formulae(self, chebi_ids):
        '''Returns all formulae'''
        all_formulae = [self.get_formulae(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_formulae for x in sublist]


    def get_mass(self, chebi_id):
        '''Returns mass'''
        if not self._MASSES:
            self._parse_chemical_data()
        return self._MASSES[chebi_id] if chebi_id in self._MASSES else float('NaN')


    def get_charge(self, chebi_id):
        '''Returns charge'''
        if not self._CHARGES:
            self._parse_chemical_data()
        return self._CHARGES[chebi_id] if chebi_id in self._CHARGES else float('NaN')


    def get_comments(self, chebi_id):
        '''Returns comments'''
        if not self._COMMENTS:
            self._parse_comments()
        return self._COMMENTS[chebi_id] if chebi_id in self._COMMENTS else []


     def get_all_comments(self, chebi_ids):
        '''Returns all comments'''
        all_comments = [self.get_comments(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_comments for x in sublist]


    def get_compound_origins(self, chebi_id):
        '''Returns compound origins'''
        if not self._COMPOUND_ORIGINS:
            self._parse_compound_origins()
        return self._COMPOUND_ORIGINS[chebi_id] if chebi_id in \
            self._COMPOUND_ORIGINS else []


    def get_all_compound_origins(self, chebi_ids):
        '''Returns all compound origins'''
        all_compound_origins = [self.get_compound_origins(chebi_id)
                                for chebi_id in chebi_ids]
        return [x for sublist in all_compound_origins for x in sublist]


    def get_status(self, chebi_id):
        '''Returns status'''
        if not self._STATUSES:
            self._parse_compounds()
        return self._STATUSES[chebi_id] if chebi_id in self._STATUSES else None


    def get_source(self, chebi_id):
        '''Returns source'''
        if not self._SOURCES:
            self._parse_compounds()
        return self._SOURCES[chebi_id] if chebi_id in self._SOURCES else None


    def get_parent_id(self, chebi_id):
        '''Returns parent id'''
        if not self._PARENT_IDS:
            self._parse_compounds()
        return self._PARENT_IDS[chebi_id] if chebi_id in self._PARENT_IDS else float('NaN')


    def get_all_ids(self, chebi_id):
        '''Returns all ids'''
        if not self._ALL_IDS:
            self._parse_compounds()
        return self._ALL_IDS[chebi_id] if chebi_id in self._ALL_IDS else []


    def get_name(self, chebi_id):
        '''Returns name'''
        if not self._NAMES:
            self._parse_compounds()
        return self._NAMES[chebi_id] if chebi_id in self._NAMES else None


    def get_definition(self, chebi_id):
        '''Returns definition'''
        if not self._DEFINITIONS:
           self._parse_compounds()
        return self._DEFINITIONS[chebi_id] if chebi_id in self._DEFINITIONS else None


    def get_modified_on(self, chebi_id):
        '''Returns modified on'''
        if not self._MODIFIED_ONS:
            self._parse_compounds()
        return self._MODIFIED_ONS[chebi_id] if chebi_id in self._MODIFIED_ONS else None


    def get_all_modified_on(self, chebi_ids):
        '''Returns all modified on'''
        all_modified_ons = [self.get_modified_on(chebi_id) for chebi_id in chebi_ids]
        all_modified_ons = [modified_on for modified_on in all_modified_ons
                            if modified_on is not None]
        return None if not all_modified_ons else sorted(all_modified_ons)[-1]


    def get_created_by(self, chebi_id):
        '''Returns created by'''
        if not self._CREATED_BYS:
            self._parse_compounds()
        return self._CREATED_BYS[chebi_id] if chebi_id in self._MODIFIED_ONS else None


    def get_star(self, chebi_id):
        '''Returns star'''
        if not self._STARS:
            self._parse_compounds()
        return self._STARS[chebi_id] if chebi_id in self._STARS else float('NaN')


    def _put_all_ids(self, parent_id, child_id):
        '''Add a parent and child id to the list of all ids'''
        if parent_id in self._ALL_IDS:
            self._ALL_IDS[parent_id].append(child_id)
        else:
            self._ALL_IDS[parent_id] = [child_id]


    def get_database_accessions(self, chebi_id):
        '''Returns database accession'''
        if not self._DATABASE_ACCESSIONS:
            self._parse_database_accessions()

        return self._DATABASE_ACCESSIONS[chebi_id] if chebi_id in \
            self._DATABASE_ACCESSIONS else []


    def get_all_database_accessions(self, chebi_ids):
        '''Returns all database accessions'''
        all_database_accessions = [self.get_database_accessions(chebi_id)
                                   for chebi_id in chebi_ids]
        return [x for sublist in all_database_accessions for x in sublist]


    def get_inchi(self, chebi_id):
        '''Returns InChI string'''
        if not self._INCHIS:
            self._parse_inchi()
        return self._INCHIS[chebi_id] if chebi_id in self._INCHIS else None


    def get_names(self, chebi_id):
        '''Returns names'''
        if not self._ALL_NAMES:
            self._parse_names()
        return self._ALL_NAMES[chebi_id] if chebi_id in self._ALL_NAMES else []


    def get_all_names(self, chebi_ids):
        '''Returns all names'''
        all_names = [self.get_names(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_names for x in sublist]


    def get_outgoings(self, chebi_id):
        '''Returns outgoings'''
        if not self._OUTGOINGS:
            self._parse_relation()
        return self._OUTGOINGS[chebi_id] if chebi_id in self._OUTGOINGS else []


    def get_all_outgoings(self, chebi_ids):
        '''Returns all outgoings'''
        all_outgoings = [self.get_outgoings(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_outgoings for x in sublist]


    def get_incomings(self, chebi_id):
        '''Returns incomings'''
        if not self._INCOMINGS:
            self._parse_relation()
        return self._INCOMINGS[chebi_id] if chebi_id in self._INCOMINGS else []


    def get_all_incomings(self, chebi_ids):
        '''Returns all incomings'''
        all_incomings = [self.get_incomings(chebi_id) for chebi_id in chebi_ids]
        return [x for sublist in all_incomings for x in sublist]


    def get_inchi_key(self, chebi_id):
        '''Returns InChI key'''
        if not self._INCHI_KEYS:
            self._parse_structures()
        return self._INCHI_KEYS[chebi_id] if chebi_id in self._INCHI_KEYS else None


    def get_smiles(self, chebi_id):
        '''Returns InChI key'''
        if not self._SMILES:
            self._parse_structures()
        return self._SMILES[chebi_id] if chebi_id in self._SMILES else None


    def _get_last_update_time(self):
        '''Returns last FTP site update time'''
        now = datetime.datetime.utcnow()

        # Get the first Tuesday of the month
        first_tuesday = self._get_first_tuesday(now)

        if first_tuesday < now:
            return first_tuesday

        first_of_month = datetime.datetime(now.year, now.month, 1)
        last_month = first_of_month + datetime.timedelta(days=-1)
        return self._get_first_tuesday(last_month)


    def _get_first_tuesday(self, this_date):
        '''Get the first Tuesday of the month'''
        month_range = calendar.monthrange(this_date.year, this_date.month)
        first_of_month = datetime.datetime(this_date.year, this_date.month, 1)
        first_tuesday_day = (calendar.TUESDAY - month_range[0]) % 7
        first_tuesday = first_of_month + datetime.timedelta(days=first_tuesday_day)
        return first_tuesday

    def _is_default_structure(self, def_struct):
        '''Is default structure?'''
        return def_struct.upper() == 'Y'
