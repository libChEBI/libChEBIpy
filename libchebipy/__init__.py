'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import json
from six.moves.urllib.parse import quote as url_quote
from six.moves.urllib.request import urlopen

from ._chebi_entity import ChebiEntity
from ._chebi_entity import ChebiException
from ._comment import Comment
from ._compound_origin import CompoundOrigin
from ._database_accession import DatabaseAccession
from ._formula import Formula
from ._name import Name
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
]


def search(term, exact=False):
    '''Searches ChEBI via ols.'''
    url = 'http://www.ebi.ac.uk/ols/api/search?ontology=chebi' + \
        '&exact=' + str(exact) + '&queryFields=label&q=' + url_quote(term)

    response = urlopen(url)
    data = json.loads(response.read())

    return [ChebiEntity(doc['obo_id']) for doc in data['response']['docs']]
