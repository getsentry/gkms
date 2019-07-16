from setuptools import find_packages, setup


setup(
    name='gkms',
    version='0.0.1',
    author='zylphrex',
    author_email='zylphrex@gmail.com',
    maintainer='zylphrex',
    maintainer_email='zylphrex@gmail.com',
    url='https://github.com/getsentry/gkms',
    description='A simple utility for using GCP Cloud KMS to encrypt and decrypt secrets and storing them in GCS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
    ],
    platforms=[
        'MacOS',
        'Unix',
        'Windows',
    ],
    keywords=[
        'cloud'
        'gcp',
        'gcs',
        'google',
        'google-cloud-kms',
        'google-cloud-storage',
        'kms',
        'encrypt',
        'decrypt',
    ],
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    install_requires=open('requirements.txt').read().split('\n'),
    entry_points={
        'console_scripts': ['gkms=gkms.cli:main'],
    }
)
