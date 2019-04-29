from setuptools import setup

requires = [
    'PySide2',
]

setup(
    name='mailprep',
    author='James Payne',
    author_email='contact@jepaynedev.com',
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'mailprep = mailprep:main',
        ],
    },
)
