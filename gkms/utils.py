import base64
import json
import sys

from contextlib import contextmanager

from google.cloud import kms
from google.cloud import storage


@contextmanager
def open_file(file_name, mode='r'):
    if file_name == '-':
        if mode == 'r':
            yield sys.stdin
        elif mode == 'a':
            yield sys.stdout
        else:
            raise ValueError('Invalid file mode: {}'.format(mode))
    else:
        with open(file_name, mode) as opened_file:
            yield opened_file


def get_unversioned_key(project, location, keyring, cryptokey):
    key_pieces = [
        'projects/{}'.format(project),
        'locations/{}'.format(location),
        'keyRings/{}'.format(keyring),
        'cryptoKeys/{}'.format(cryptokey),
    ]
    return '/'.join(key_pieces)


def download(project, bucket_name, blob_name, client=None):
    if client is None:
        client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        raise ValueError('Bucket {} does not exist!'.format(bucket_name))
    blob = bucket.get_blob(blob_name)
    if not blob:
        raise ValueError('Blob {} does not exist!'.format(blob_name))
    return blob.download_as_string().decode('utf-8')


def upload(project, bucket_name, blob_name, string, client=None):
    if client is None:
        client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        bucket.create()
    blob = bucket.blob(blob_name)
    blob.upload_from_string(string)


def save_secret(project, bucket, target, encrypted, key, client=None):  # pylint: disable=too-many-arguments
    secret = json.dumps({
        'secret': encrypted,
        'key': key,
    })
    upload(project, bucket, target, secret, client=client)


def encrypt_secret(key, secret, client=None):
    if client is None:
        client = kms.KeyManagementServiceClient()
    secret_bytes = bytes(secret, 'ascii')
    encrypted = client.encrypt(key, secret_bytes)
    return base64.b64encode(encrypted.ciphertext).decode('utf-8')


def get_secret(project, bucket_name, blob_name, client=None):
    blob = download(project, bucket_name, blob_name, client=client)
    secret = json.loads(blob)
    secret['secret'] = base64.b64decode(secret['secret'])
    return secret


def decrypt_secret(key, secret, client=None):
    if client is None:
        client = kms.KeyManagementServiceClient()
    decrypted = client.decrypt(key, secret)
    return decrypted.plaintext.decode('utf-8')
