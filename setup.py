import setuptools

setuptools.setup(
    name="cheminventory",
    version="0.1.0",
    url="https://github.com/marcosfelt/cheminventory",

    author="Kobi Felton",
    author_email="kobi.c.f@gmail.com",

    description="A CLI and SDK for ChemInventory",
    long_description=open('README.md').read(),

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
