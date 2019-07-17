import base64
import json

from gkms.utils import open_file
from gkms.utils import get_key
from gkms.utils import encrypt_secret
from gkms.utils import save_secret


def encrypt_cmd(args):
    encrypt(args.project, args.location, args.ring,
                 args.key, args.version, args.bucket,
                 args.target, args.secret)


def encrypt(project, location, keyring, cryptokey,
            version, bucket, target, secret_name):
    versioned_key, unversioned_key = get_key(project, location, keyring,
                                             cryptokey, version)

    with open_file(secret_name) as f:
        unencrypted = f.read()

    encrypted = encrypt_secret(versioned_key, unencrypted)
    save_secret(project, bucket, target, encrypted, unversioned_key)
