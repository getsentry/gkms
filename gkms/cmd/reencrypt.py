from google.cloud import kms
from google.cloud import storage

from gkms.utils import decrypt_secret
from gkms.utils import encrypt_secret
from gkms.utils import get_secret
from gkms.utils import save_secret

def reencrypt_cmd(args):
    reencrypt(args.project, args.bucket, args.target)


def reencrypt(project, bucket, target):
    storage_client = storage.Client(project=project)
    secret = get_secret(project, bucket, target, client=storage_client)
    encrypted = secret['secret']
    key = secret['key']

    kms_client = kms.KeyManagementServiceClient()
    primary_key = kms_client.get_crypto_key(key).primary.name

    decrypted = decrypt_secret(key, encrypted, client=kms_client)
    encrypted = encrypt_secret(primary_key, decrypted, client=kms_client)
    save_secret(project, bucket, target, encrypted, key, client=storage_client)
