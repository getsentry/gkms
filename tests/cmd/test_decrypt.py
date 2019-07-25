import base64
import json

from unittest import TestCase
from unittest.mock import Mock, PropertyMock, patch

from pytest import raises

from gkms.cmd.decrypt import decrypt, download


class TestDownload(TestCase):
    def test_missing_bucket(self):
        with patch('gkms.cmd.decrypt.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=False):
                with raises(ValueError):
                    download('my-project', 'my-bucket', 'my-blob')

    def test_missing_blob(self):
        with patch('gkms.cmd.decrypt.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=True):
                with patch.object(storage.Client().bucket(), 'get_blob', return_value=None):
                    with raises(ValueError):
                        download('my-project', 'my-bucket', 'my-blob')

    def test_download_as_string(self):
        with patch('gkms.cmd.decrypt.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=True):
                blob = Mock()
                with patch.object(storage.Client().bucket(), 'get_blob', return_value=blob):
                    download('my-project', 'my-bucket', 'my-blob')
                    blob.download_as_string.assert_called_once_with()


class TestDecrypt(TestCase):
    def test_decryps_downloaded_json(self):
        cipher = json.dumps({
            'secret': base64.b64encode(b'this is the cipher text').decode('utf-8'),
            'key': 'this is the key',
        })
        with patch('gkms.cmd.decrypt.download', return_value=cipher):
            with patch('gkms.cmd.decrypt.kms') as kms:
                mock = Mock()
                secret = b'im whats in the secret'
                type(mock).plaintext = PropertyMock(return_value=secret)
                with patch.object(kms.KeyManagementServiceClient(), 'decrypt', return_value=mock) as kms_decrypt:
                    decrypted = decrypt('my-project', 'my-bucket', 'my-blob')
                    assert decrypted == secret.decode('utf-8')

