from google.cloud import kms

from gkms.utils import open_file
from gkms.utils import get_unversioned_key
from gkms.utils import encrypt_secret
from gkms.utils import save_secret


def encrypt_cmd(args):
    encrypt(args.project, args.location, args.ring,
            args.key, args.bucket, args.target, args.secret)


def encrypt(project, location, keyring, cryptokey,  # pylint: disable=too-many-arguments
            bucket, target, secret_name):
    unversioned_key = get_unversioned_key(project, location,
                                          keyring, cryptokey)
    kms_client = kms.KeyManagementServiceClient()
    versioned_key = kms_client.get_crypto_key(unversioned_key).primary.name

    with open_file(secret_name) as secret_file:
        unencrypted = secret_file.read()

    encrypted = encrypt_secret(versioned_key, unencrypted, client=kms_client)
    save_secret(project, bucket, target, encrypted, unversioned_key)
