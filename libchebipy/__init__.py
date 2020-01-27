'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import json

import requests

from ._chebi_entity import ChebiEntity
from ._chebi_entity import ChebiException
from ._comment import Comment
from ._compound_origin import CompoundOrigin
from ._database_accession import DatabaseAccession
from ._formula import Formula
from ._name import Name
from ._parsers import set_auto_update, set_download_cache_path
from ._reference import Reference
from ._relation import Relation
from ._structure import Structure


__all__ = [
    "ChebiEntity",
    "ChebiException",
    "Comment",
    "CompoundOrigin",
    "DatabaseAccession",
    "Formula",
    "Name",
    "Reference",
    "Relation",
    "Structure",
    "search",
    "set_auto_update",
    "set_download_cache_path",
]


def search(term, exact=False, rows=1e6):
    '''Searches ChEBI via ols.'''
    term = term if exact else '"' + term + '"'

    url = 'https://www.ebi.ac.uk/ols/api/search?ontology=chebi' + \
        '&exact=' + str(exact) + '&q=' + term + \
        '&rows=' + str(int(rows))

    response = requests.get(url)
    data = response.json()

    return [ChebiEntity(doc['obo_id']) for doc in data['response']['docs']]
