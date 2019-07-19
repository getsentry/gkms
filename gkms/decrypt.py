import base64
import json

from google.cloud import kms
from google.cloud import storage


def decrypt_cmd(args):
    print(decrypt(args.project, args.bucket, args.target))


def download(project, bucket_name, blob_name):
    client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        raise ValueError('Bucket {} does not exist!'.format(bucket_name))
    blob = bucket.get_blob(blob_name)
    if not blob:
        raise ValueError('Blob {} does not exist!'.format(blob_name))
    return blob.download_as_string().decode('utf-8')


def decrypt(project, bucket, target):
    blob = download(project, bucket, target)
    secret = json.loads(blob)
    encrypted = base64.b64decode(secret['secret'])
    key = secret['key']

    client = kms.KeyManagementServiceClient()
    secret = client.decrypt(key, encrypted)
    return secret.plaintext.decode('utf-8')
