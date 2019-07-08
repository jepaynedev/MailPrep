#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import glob
import os.path

import setuptools
import setuptools.command.install

requires = [
    'PySide2',
    'pyyaml',
]


dev_extras = [
    'pytest',
    'tox',
    'tox-venv',
]


class Pyside2UICRunnerOnInstall(setuptools.command.install.install):
    def run(self):
        from pyside2_uic_runner import run_pyside2_uic
        run_pyside2_uic('ui/', 'src/mailprep/ui/')
        setuptools.command.install.install.run(self)

setuptools.setup(
    name='mailprep',
    version='0.0',
    description='List preparation for UW Extension Bulk Mail Center',
    author='James Payne',
    author_email='contact@jepaynedev.com',
    license='MIT',
    python_requires='>=3.4',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0]
        for path in glob.glob('src/*.py')
    ],
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
        'install': Pyside2UICRunnerOnInstall,
    },
    entry_points={
        'console_scripts': [
            'mailprep = mailprep:main',
        ],
    },
)
