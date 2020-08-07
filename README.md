# libChEBIpy
libChEBIpy: a Python API for accessing the ChEBI database

Details of the API are available: http://libchebi.github.io/libChEBI%20API.pdf

## Environment

To customize the root of the download directory, set the following environment variable:

```bash
export LIBCHEBIPY_DOWNLOAD_DIR=/path/to/folder
```

if not set, the library will default to the folder `libChEBI` in the user's home,
e.g., `/home/<username>/libChEBI`.

## Custom Storage

The library has a set of [parsers](libchebipy/_parsers) that include:

 - [A local filesystem cache](libchebipy/_parsers/filesystem.py)
 - [Google Storage](libchebipy/_parsers/googlestorage.py)


### Filesystem

This is the default parser, and (as stated above) you can customize the download
directory either by exporting `LIBCHEBIPY_DOWNLOAD_DIR` to the environment, or by
instantiating a ChebiClient with it as follows:

```python
from libchebipy._chebi_entity import ChebiEntity
chebi_entity = ChebiEntity(15903, download_dir="/path/to/directory")
```

The above is equivalent to selected a filesystem parser (the default):

```python
chebi_entity = ChebiEntity(15903, download_dir="/path/to/directory", parser="filesystem")
```

### Google Storage

If you don't want to use a filesystem cache, or otherwise want to use a Google 
Storage cache, then you can initialize your ChebiEntity to use a `googlestorage` parser:

```python
from libchebipy import ChebiEntity
chebi_entity = ChebiEntity("15903", parser="googlestorage")
```

You need a few extra Python modules installed for the Google Storage client and
[gs-chunked-io](https://github.com/xbrianh/gs-chunked-io):

```bash
pip install gs-chunked-io
pip install google-cloud-storage
```

You are required to have your `GOOGLE_APPLICATION_CREDENTIALS` (the path to the json
file with your credentials) exported to the environment, along with the name
of the Google Storage bucket. To take a more conservative approach, the bucket must
exist. You can create a bucket in the Google Cloud [console](https://console.cloud.google.com/storage/browser/)
and then export your variables as follows:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=$PWD/auth/credentials.json
export GOOGLE_STORAGE_BUCKET=libchebi-testing
```

If you want a storage prefix (akin to a "folder" in your bucket) you can
export:

```baah
export STORAGE_PREFIX=libchebi-cache
```

We would then import ChebiEntity, which will find the parsers already in the namespace 
and not re-import (and thus override your custom function):

```python
from libchebipy import ChebiEntity
```

Then initialize a ChebiEntity, but set the parser to be googlestorage.

```python
entity = ChebiEntity('CHEBI:15365', parser="googlestorage")
```

If your environment variables aren't defined for the bucket or credentials, you'll
get an error. Note that the Google Storage parser still requires write access to
a temporary directory to read the files from.

### Improvements

It's possible to extract content directly into Google Storage, that would look like this:

```python
# If the blob is a zip file, extract into storage
if filepath.endswith('.zip'):
    with gscio.AsyncReader(blob) as fh:
        zfile = zipfile.ZipFile(fh)
        filepath = zfile.namelist()[0]
        for contentfilename in myzip.namelist():
            contentfile = zfile.read(contentfilename)
            nested_blob = self.bucket.blob(self.bucket_name + "/" + contentfilename)
            nested_blob.upload_from_string(contentfile)

elif filepath.endswith('.gz'):
    unzipped_filepath = filename[:-len('.gz')]
    filepath = unzipped_filepath

    # Checks if exists, and timestamp
    if not self._is_current(unzipped_filepath):
        unzipped_blob = self.bucket.blob(unzipped_filepath)
        with gscio.AsyncReader(blob) as fh:
            gzip_reader = gzip.GzipFile(fileobj=fh)
            unzipped_blob.upload_from_string(gzip_reader.read())

```

However, we would ultimately still need to write these files to a temporary location
to allow for custom reading with different encodings, e.g., something like this:

```bash
with io.open(filename, "r", encoding="cp1252") as textfile:
    next(textfile)
```

So if you are able to reproduce that but getting content directly from a Google
Storage read, then the Google Storage client would not need to write anything
to a temporary file. Please open a pull request if you can contribute this change!

