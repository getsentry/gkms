from gkms.cmd.decrypt import decrypt
from gkms.cmd.encrypt import encrypt
from gkms.cmd.reencrypt import reencrypt


def get(project, bucket, target, default=None):
    try:
        return decrypt(project, bucket, target)
    except ValueError:
        return default
