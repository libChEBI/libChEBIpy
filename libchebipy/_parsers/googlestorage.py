"""
libChEBIpy (c) University of Manchester 2015-2020

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
"""

import os.path
import tempfile
import shutil

import six.moves.urllib.parse as urlparse

from google.cloud import storage
import gs_chunked_io as gscio
import urllib

from .base import ParserBase


class GoogleStorageCache(ParserBase):
    """Save files in a Google Storage bucket. Since this is likely to use
       app engine (which does not have write to the filesystem) we do most
       work in memory.
    """

    def __init__(self, download_dir=None, auto_update=True):
        super().__init__(download_dir, auto_update)
        self._init_bucket()
        self.path = None
        self.download_dir = tempfile.mkdtemp()

    def _init_bucket(self):
        """Given a GOOGLE_STORAGE_BUCKET in the environment, make a connection
           to it.
        """
        self.bucket_name = os.environ.get("GOOGLE_STORAGE_BUCKET")
        self.storage_prefix = os.environ.get("GOOGLE_STORAGE_PREFIX", "").strip("/")
        if not self.bucket_name:
            raise ValueError(
                "GOOGLE_STORAGE_BUCKET is required to be exported in the environment."
            )

        # Instantiates a client to connect to a Google Storage Bucket
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def __del__(self):
        """Cleanup when the instance is destroyed
        """
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)

    def get_file(self, filename):
        """Downloads filename from ChEBI FTP site and saves to Google Storage"""
        filename = os.path.join(self.storage_prefix, filename)
        filepath = os.path.join(self.bucket_name, filename)

        # If the temporary download exists, use it
        tmpfile = os.path.join(self.download_dir, os.path.basename(filepath))
        if os.path.exists(tmpfile):
            return tmpfile

        # The blob in storage
        blob = self.bucket.blob(filename)

        # If the blob doesn't exist or is not current
        if not self._is_current(filepath):

            url = (
                "ftp://ftp.ebi.ac.uk/pub/databases/chebi/" + "Flat_file_tab_delimited/"
            )

            # Upload the original file
            response = urllib.request.urlopen(urlparse.urljoin(url, filename))
            with gscio.Writer(filename, self.bucket) as fh:
                fh.write(response.read())

        # Write to temporary location
        blob.download_to_filename(tmpfile)
        return self._extract_compressed_file(tmpfile, self.download_dir)

    def _is_current(self, filepath):
        """Checks whether file is current"""
        if not self.auto_update:
            return True

        # Check if the blob exists
        blob = self.bucket.blob(filepath)
        if not blob.exists():
            return False

        # Make sure we have updated metadata
        blob.update()

        # This technically shouldn't happen, but might be an edge case
        if not blob.time_created:
            return False

        return blob.time_created.utcnow() > self._get_last_update_time()
