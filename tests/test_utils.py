import base64
import json

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import PropertyMock
from unittest.mock import patch

from pytest import raises

from gkms.utils import open_file
from gkms.utils import get_key
from gkms.utils import download
from gkms.utils import upload
from gkms.utils import save_secret
from gkms.utils import encrypt_secret
from gkms.utils import get_secret
from gkms.utils import decrypt_secret


class TextOpenFile(TestCase):
    def test_stdin(self):
        with patch('gkms.utils.sys.stdin') as stdin:
            with open_file('-') as f:
                assert f is stdin

            with open_file('-', 'r') as f:
                assert f is stdin

    def test_stdout(self):
        with patch('gkms.utils.sys.stdout') as stdout:
            with open_file('-', 'a') as f:
                assert f is stdout

    def test_std_bad_mode(self):
        with raises(ValueError):
            with open_file('-', 'x') as f:
                assert f is stdin


class TestGetKey(TestCase):
    def test_get_key(self):
        with_version, without_version = get_key('my-project', 'my-location', 'my-key-ring', 'my-crypto-key', 'my-version')
        assert with_version == 'projects/my-project/locations/my-location/keyRings/my-key-ring/cryptoKeys/my-crypto-key/cryptoKeyVersions/my-version'
        assert without_version == 'projects/my-project/locations/my-location/keyRings/my-key-ring/cryptoKeys/my-crypto-key'


class TestDownload(TestCase):
    def test_missing_bucket(self):
        with patch('gkms.utils.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=False):
                with raises(ValueError):
                    download('my-project', 'my-bucket', 'my-blob')

    def test_missing_blob(self):
        with patch('gkms.utils.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=True):
                with patch.object(storage.Client().bucket(), 'get_blob', return_value=None):
                    with raises(ValueError):
                        download('my-project', 'my-bucket', 'my-blob')

    def test_download_as_string(self):
        with patch('gkms.utils.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=True):
                blob = Mock()
                with patch.object(storage.Client().bucket(), 'get_blob', return_value=blob):
                    download('my-project', 'my-bucket', 'my-blob')
                    blob.download_as_string.assert_called_once_with()


class TestUpload(TestCase):
    def test_upload_as_string(self):
        with patch('gkms.utils.storage') as storage:
            with patch.object(storage.Client().bucket().blob(), 'upload_from_string') as upload_from_string:
                upload('my-project', 'my-bucket', 'my-blob', 'my-string')
                upload_from_string.assert_called_once_with('my-string')

    def test_creates_new_bucket(self):
        with patch('gkms.utils.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=False):
                with patch.object(storage.Client().bucket(), 'create') as create:
                    upload('my-project', 'my-bucket', 'my-blob', 'my-string')
                    create.assert_called_once_with()

    def test_use_existing_bucket(self):
        with patch('gkms.utils.storage') as storage:
            with patch.object(storage.Client().bucket(), 'exists', return_value=True):
                with patch.object(storage.Client().bucket(), 'create') as create:
                    upload('my-project', 'my-bucket', 'my-blob', 'my-string')
                    assert not create.called


class TestSaveSecret(TestCase):
    def test_uploads_json_dump(self):
        with patch('gkms.utils.upload') as upload:
            save_secret('my-project', 'my-bucket', 'my-blob', 'my encrypted secret', 'my-key')
            dump = json.dumps({
                'secret': 'my encrypted secret',
                'key': 'my-key',
            })
            upload.assert_called_once_with('my-project', 'my-bucket', 'my-blob', dump, client=None)


class TestEncryptSecret(TestCase):
    def test_base64_secret(self):
        with patch('gkms.utils.kms') as kms:
            secret = Mock()
            cipher = b'my secret'
            type(secret).ciphertext = cipher
            with patch.object(kms.KeyManagementServiceClient(), 'encrypt', return_value=secret) as encrypt:
                b64 = encrypt_secret('my-key', cipher.decode('utf-8'))
                assert b64 == base64.b64encode(cipher).decode('utf-8')


class TestGetSecret(TestCase):
    def test_get_decrypted_json(self):
        secret = 'my big secret'
        blob = json.dumps({
            'key': 'my-key',
            'secret': base64.b64encode(bytes(secret, 'ascii')).decode('utf-8'),
        })
        with patch('gkms.utils.download', return_value=blob) as download:
            secret_blob = get_secret('my-project', 'my-bucket', 'my-blob')
            assert secret == secret_blob['secret'].decode('utf-8')
            assert 'my-key' == secret_blob['key']


class TestDecryptSecret(TestCase):
    def test_plain_text_secret(self):
        with patch('gkms.utils.kms') as kms:
            secret = Mock()
            plaintext = 'im the secret'
            type(secret).plaintext = bytes(plaintext, 'ascii')
            with patch.object(kms.KeyManagementServiceClient(), 'decrypt', return_value=secret) as decrypt:
                assert plaintext == decrypt_secret('my-key', 'its a biiiig secret')
