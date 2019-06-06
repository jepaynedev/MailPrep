#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install as InstallCommand

requires = [
    'PySide2',
]


dev_extras = [
    'pytest',
    'tox',
    'tox-venv',
]


class CustomInstallCommand(InstallCommand):
    def run(self):
        import subprocess
        for path in glob('ui/*.ui'):
            result = subprocess.run(['pyside2-uic', path], capture_output=True)
            output_path = f'src/mailprep/ui/{splitext(basename(path))[0]}_ui.py'
            with open(output_path, 'w') as output_file:
                data = result.stdout.decode()
                output_file.write(data)
        InstallCommand.run(self)

setup(
    name='mailprep',
    version='0.0',
    description='List preparation for UW Extension Bulk Mail Center',
    author='James Payne',
    author_email='contact@jepaynedev.com',
    license='MIT',
    python_requires='>=3.4',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Win32',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=requires,
    extras_require={
        'dev': dev_extras,
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'mailprep = mailprep:main',
        ],
    },
)
