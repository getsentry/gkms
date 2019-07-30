import argparse

from gkms.cmd.decrypt import decrypt_cmd
from gkms.cmd.encrypt import encrypt_cmd
from gkms.cmd.reencrypt import reencrypt_cmd


AVAILABLE_COMMANDS = {
    'decrypt': decrypt_cmd,
    'encrypt': encrypt_cmd,
    'reencrypt': reencrypt_cmd,
}


def dispatch(args):
    cmd = AVAILABLE_COMMANDS[args.command]
    cmd(args)


def main():
    ################################################################################################
    # Main Parser
    ################################################################################################

    description = 'Utility for encrypting secrets using GCP\'s KMS and storing it in GCS.'
    parser = argparse.ArgumentParser(description=description)

    subparser = parser.add_subparsers(title='subcommands', dest='command')
    subparser.required = True  # NOTE: For backward compatibility, only available as a kwarg in 3.7+

    ################################################################################################
    # Decrypt Parser
    ################################################################################################

    description = 'Download and decrypt secrets'
    decrypt_parser = subparser.add_parser('decrypt', help=description)

    description = 'The GCP project to use.'
    decrypt_parser.add_argument('-p', '--project', metavar='project',
                                type=str, required=True, help=description)

    description = 'The GCS bucket that holds the secret'
    decrypt_parser.add_argument('-b', '--bucket', metavar='bucket',
                                type=str, required=True, help=description)

    description = 'The GCS object that holds the secret'
    decrypt_parser.add_argument('-t', '--target', metavar='target',
                                type=str, required=True, help=description)

    ################################################################################################
    # Encrypt Parser
    ################################################################################################

    description = 'Encrypt and upload secrets'
    encrypt_parser = subparser.add_parser('encrypt', help=description)

    description = 'The GCP project to use.'
    encrypt_parser.add_argument('-p', '--project', metavar='project',
                                type=str, required=True, help=description)

    description = 'The location of the key ring.'
    encrypt_parser.add_argument('-l', '--location', metavar='location',
                                type=str, required=True, help=description)

    description = 'The key ring name.'
    encrypt_parser.add_argument('-r', '--ring', metavar='keyring',
                                type=str, required=True, help=description)

    description = 'The key name.'
    encrypt_parser.add_argument('-k', '--key', metavar='cryptokey',
                                type=str, required=True, help=description)

    description = 'The file containing the secret. Use - for stdin.'
    encrypt_parser.add_argument('-s', '--secret', metavar='secret',
                                type=str, required=True, help=description)

    description = 'The GCS bucket to hold the secret'
    encrypt_parser.add_argument('-b', '--bucket', metavar='bucket',
                                type=str, required=True, help=description)

    description = 'The target file name to store the secret.'
    encrypt_parser.add_argument('-t', '--target', metavar='target',
                                type=str, required=True, help=description)

    ################################################################################################
    # Rotate Parser
    ################################################################################################

    description = 'Reencrypt the secret using the latest primary key'
    reencrypt_parser = subparser.add_parser('reencrypt', help=description)

    description = 'The GCP project to use.'
    reencrypt_parser.add_argument('-p', '--project', metavar='project',
                                  type=str, required=True, help=description)

    description = 'The GCS bucket that holds the secret'
    reencrypt_parser.add_argument('-b', '--bucket', metavar='bucket',
                                  type=str, required=True, help=description)

    description = 'The GCS object that holds the secret.'
    reencrypt_parser.add_argument('-t', '--target', metavar='target',
                                  type=str, required=True, help=description)

    ################################################################################################
    # Dispatch Commands
    ################################################################################################

    args = parser.parse_args()
    dispatch(args)


if __name__ == '__main__':
    main()
