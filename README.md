# libChEBIpy
libChEBIpy: a Python API for accessing the ChEBI database

Details of the API are available: http://libchebi.github.io/libChEBI%20API.pdf


## Custom Storage

While there isn't native support for custom storage, you can easily implement
your own function to retrieve a file and save to a custom storage. As an example,
you might first import the library's parsers:

```python
import sys
import libchebipy._parsers as parsers
```

And note that the parsers have a default get_file function that is used throughout the module.
```python
parsers.get_file                                                                                                       
<function libchebipy._parsers.get_file(filename)>
```

You might then decide to write your own custom function, which should generally
perform the same operations as the original. As a dummy example of this working, we 
can write a simply function that just prints the filename for the user. We also
add a sys.exit since this function obviously doesn't work and we don't want the 
execution to continue after running it.

```python
def get_file(filename):
    print(filename)
    sys.exit(0)
```

And then override the function for the parsers

```python
parsers.get_file = get_file
```

We would then import ChebiEntity, which will find the parsers already in the namespace 
and not re-import (and thus override your custom function):

```python
from libchebipy import ChebiEntity
```

We don't need to do a lot to see our function is working!

```python
entity = ChebiEntity('CHEBI:15365')

compounds.tsv.gz
An exception has occurred, use %tb to see the full traceback.

SystemExit: 0
```

But more realistically we want a custom storage that works! The following
example for Google Storage is provided.

### Google Storage

This example assumes that you have exported your `GOOGLE_APPLICATION_CREDENTIALS`
and have created a bucket in Google Storage that the credentials have write permission to.
Again, the function here should take the relative name of a filepath in the 
expected storage. This example uses [gs-chunked-io](https://github.com/xbrianh/gs-chunked-io)
to write directly from memory to storage.

```python
from google.cloud import storage
import gs_chunked_io as gscio
import zipfile
import urllib

def get_file(filename):
    '''Downloads filename from ChEBI FTP site and saves to Google Storage'''

    # Instantiates a client to connect to a Google Storage Bucket
    bucket_name = "libchebi-bucket"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    filepath = os.path.join(bucket_name, filename)

    # The blob in storage
    blob = bucket.blob(filename)

    # If the blob doesn't exist, 
    if not blob.exists():

        url = 'ftp://ftp.ebi.ac.uk/pub/databases/chebi/' + \
            'Flat_file_tab_delimited/'

        response = urllib.request.urlopen(urlparse.urljoin(url, filename))
        chunk_size = 16 * 1024

        # Stream the response into a blob
        with gscio.Writer(filename, bucket) as fh_write:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                fh_write(chunk)

    # If the blob is a zip file, extract into storage
    if filepath.endswith('.zip'):
        with gscio.AsyncReader(blob) as fh:
            zfile = zipfile.ZipFile(fh)
            for contentfilename in myzip.namelist():
                contentfile = zfile.read(contentfilename)
                nested_blob = bucket.blob(bucket_name + "/" + contentfilename)
                blob.upload_from_string(contentfile)

    elif filepath.endswith('.gz'):
        unzipped_filepath = filepath[:-len('.gz')]
        unzipped_blob = bucket.blob(unzipped_filepath)
        if not unzipped_blob.exists(): 
            with gscio.AsyncReader(blob) as fh:
                gzip_reader = gzip.GzipFile(fileobj=fh)
                tf = tarfile.TarFile(fileobj=gzip_reader)
                # to be written
