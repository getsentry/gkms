# gkms

`gkms` is a simple utility for using GCP Cloud KMS to encrypt and decrypt secrets and storing them in GCS.

## Installation

```shell
pip install gkms
```

## Setup

Please see [https://googleapis.github.io/google-cloud-python/latest/core/auth.html](https://googleapis.github.io/google-cloud-python/latest/core/auth.html) for authentication with `Google Cloud SDK`.

## Usage

### CLI

```shell
gkms encrypt --project my-gcp-project --location global --ring my-key-ring --key my-crypto-key --version 1 --bucket my-bucket --target my-target.txt --secret my-secret.txt
gkms decrypt --project my-gcp-project --bucket my-bucket --target my-target.txt
```

### Python

```python
import gkms

gkms.encrypt('my-gcp-project', 'global', 'my-key-ring', 'my-crypto-key', '1', 'my-bucket', 'my-secret.txt', 'my-secret.txt')
decrypted = gkms.decrypt('my-gcp-project', 'my-bucket', 'my-secret.txt')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Getting Started

Set up your virual environment however you like.

```shell
pip install -e .
pip install -r requirements-dev.txt
```

You're ready to start developing!

### Running Tests

```shell
pytest
```
