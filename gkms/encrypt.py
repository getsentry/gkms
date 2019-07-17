import base64
import json

from google.cloud import kms
from google.cloud import storage

from utils import open_file


def encrypt_cmd(args):
    encrypt(args.project, args.location, args.ring,
                 args.key, args.version, args.bucket,
                 args.target, args.secret)

def get_key(project, location, keyring, cryptokey, version):
    key_pieces = [
        'projects/{}'.format(project),
        'locations/{}'.format(location),
        'keyRings/{}'.format(keyring),
        'cryptoKeys/{}'.format(cryptokey),
        'cryptoKeyVersions/{}'.format(version),
    ]
    return '/'.join(key_pieces), '/'.join(key_pieces[:-1])


def upload(project, bucket_name, blob_name, string):
    client = storage.Client(project)
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        bucket.create()
    blob = bucket.blob(blob_name)
    blob.upload_from_string(string)


def encrypt(project, location, keyring, cryptokey,
            version, bucket, target, secret_name):
    versioned_key, unversioned_key = get_key(project, location, keyring,
                                             cryptokey, version)

    with open_file(secret_name) as f:
        unencrypted = f.read()

    client = kms.KeyManagementServiceClient()
    encrypted_bytes = client.encrypt(versioned_key, bytes(unencrypted, 'ascii'))
    encrypted = base64.b64encode(encrypted_bytes.ciphertext).decode('utf-8')

    secret = json.dumps({
        'secret': encrypted,
        'key': unversioned_key,
    })
    upload(project, bucket, target, secret)
