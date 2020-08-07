"""
libChEBIpy (c) University of Manchester 2015-2020

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
"""
import datetime
import os.path

import six.moves.urllib.parse as urlparse
from six.moves.urllib.request import urlretrieve, urlcleanup


from .base import ParserBase


class FileSystemCache(ParserBase):
    """A filesystem cache saves files on the user's local filesystem for later 
       use. The functions defined here are any from the original Parser Base
       that would warrant opening a file on the filesystem.
    """

    def __init__(self, download_dir=None, auto_update=True):
        super().__init__(download_dir, auto_update)

    def get_file(self, filename):
        """Downloads filename from ChEBI FTP site"""
        filepath = os.path.join(self.path, filename)

        if not self._is_current(filepath):
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            url = (
                "ftp://ftp.ebi.ac.uk/pub/databases/chebi/" + "Flat_file_tab_delimited/"
            )
            urlretrieve(urlparse.urljoin(url, filename), filepath)
            urlcleanup()

        return self._extract_compressed_file(filepath, self.path)

    def _is_current(self, filepath):
        """Checks whether file is current"""
        if not self.auto_update:
            return True

        if not os.path.isfile(filepath):
            return False

        return (
            datetime.datetime.utcfromtimestamp(os.path.getmtime(filepath))
            > self._get_last_update_time()
        )
