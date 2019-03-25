import setuptools


setuptools.setup(
    name="cheminventory",
    version="0.2.2",
    url="https://github.com/marcosfelt/cheminventory_python",

    author="Kobi Felton",
    author_email="kobi.c.f@gmail.com",

    description="A CLI and SDK for ChemInventory",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    packages=setuptools.find_packages(),

    install_requires=['requests'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
