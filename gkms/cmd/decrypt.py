from gkms.utils import get_secret
from gkms.utils import decrypt_secret


def decrypt_cmd(args):
    print(decrypt(args.project, args.bucket, args.target))


def decrypt(project, bucket, target):
    secret = get_secret(project, bucket, target)
    encrypted = secret['secret']
    key = secret['key']

    return decrypt_secret(key, encrypted)
