from unittest import TestCase
from unittest.mock import patch

from pytest import raises

from gkms.utils import open_file


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

