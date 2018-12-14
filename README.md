ChemInventory
=================

[![PyPI version](https://badge.fury.io/py/cheminventory.svg)](https://pypi.org/project/cheminventory/)

An unofficial python SDK for [ChemInventory](https://www.cheminventory.net/). ChemInventory is used for keeping track of chemicals in a laboratory.

Usage
-----

```python

ci = ChemInventory(email='joe@none.com', password='123456')

#Search for a CAS number
ci.search('75-65-0')

```

For more details look at the [tutorial](tutorial/tutorial.ipynb).

Installation
------------

`pip install cheminventory`


Authors
-------

This is an unofficial cheminventory package. ChemInventory and its namesake are not owned by me. 
