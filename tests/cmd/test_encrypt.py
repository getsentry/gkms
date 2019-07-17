import base64
import json

from unittest import TestCase
from unittest.mock import Mock, PropertyMock, patch

from gkms.cmd.encrypt import encrypt, get_key, upload


class TestEncrypt(TestCase):
    def test_uploads_encrypted_json(self):
        with patch('gkms.cmd.encrypt.open_file') as open_file:
            plain = 'here is some test string'
            with patch.object(open_file().__enter__(), 'read', return_value=plain):
                with patch('gkms.cmd.encrypt.kms') as kms:
                    mock = Mock()
                    cipher = b'this is the cipher text'
                    type(mock).ciphertext = PropertyMock(return_value=cipher)
                    with patch.object(kms.KeyManagementServiceClient(), 'encrypt', return_value=mock) as kms_encrypt:
                        with patch('gkms.cmd.encrypt.upload') as upload:
                            project = 'my-project'
                            key_vars = [project, 'my-location', 'my-key-ring', 'my-crypto-key', 'my-version']
                            obj_vars = ['my-bucket', 'my-target']
                            versioned_key, unversioned_key = get_key(*key_vars)
                            encrypt(*key_vars, *obj_vars, 'my-secret')
                            kms_encrypt.assert_called_once_with(versioned_key, bytes(plain, 'ascii'))
                            secret = json.dumps({
                                'secret': base64.b64encode(cipher).decode('utf-8'),
                                'key': unversioned_key
                            })
                            upload.assert_called_once_with(project, *obj_vars, secret)



class TestGetKey(TestCase):
    def test_get_key(self):
        with_version, without_version = get_key('my-project', 'my-location', 'my-key-ring', 'my-crypto-key', 'my-version')
        assert with_version == 'projects/my-project/locations/my-location/keyRings/my-key-ring/cryptoKeys/my-crypto-key/cryptoKeyVersions/my-version'
        assert without_version == 'projects/my-project/locations/my-location/keyRings/my-key-ring/cryptoKeys/my-crypto-key'


class TestUpload(TestCase):
    def test_upload_as_string(self):
        with patch('gkms.cmd.encrypt.storage') as storage:
            with patch.object(storage.Client().bucket().blob(), 'upload_from_string') as upload_from_string:
                upload('my-gcp-project', 'my-bucket', 'my-blob', 'my-string')
                upload_from_string.assert_called_once_with('my-string')

    def test_creates_new_bucket(self):
        with patch('gkms.cmd.encrypt.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=False):
                with patch.object(storage.Client().bucket(), 'create') as create:
                    upload('my-gcp-project', 'my-bucket', 'my-blob', 'my-string')
                    create.assert_called_once_with()

    def test_use_existing_bucket(self):
        with patch('gkms.cmd.encrypt.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=True):
                with patch.object(storage.Client().bucket(), 'create') as create:
                    upload('my-gcp-project', 'my-bucket', 'my-blob', 'my-string')
                    assert not create.called

