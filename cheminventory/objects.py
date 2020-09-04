import requests
import base64
class Container:

    def __init__(self, inventory_id, compound_id,
                 name, location, cas=None, smiles=None, size=None,
                 comments=None, barcode=None, supplier=None, 
                 date_acquired=None, owner=None, linked_files=None):
        self._inventory_id = inventory_id
        self._compound_id = compound_id
        self._name = name
        # if not location or isinstance(location, Location):
        #     self._location = location
        # else: 
        #     raise TypeError('Assigned location must be a Location object.')
        self._location = location
        self._smiles = smiles
        self._cas = cas
        self._size = size
        self._comments = comments
        self._barcode = barcode
        self._supplier = supplier
        self._date_acquired = date_acquired
        self._owner = owner
        self._linked_files = linked_files

    def __repr__(self):
        return f"Container {self._inventory_id}: {self._name}"

    def __eq__(self, other):
        return isinstance(other, Container) and self.inventory_id == other.inventory_id

    def _repr_png_(self):
        '''Return image for use in jupyter notebook'''
        return self.image

    @property
    def inventory_id(self):
        '''Container record ID'''
        return self._inventory_id

    @property
    def compound_id(self):
        '''Compound record ID'''
        return self._compound_id
                
    @property
    def image(self):
        '''Return an image of the structure of the compound'''
        try:
            image_url = f"https://s3.eu-central-1.amazonaws.com/chemicalinventory-structures-frankfurt/ID-{self.compound_id}-1.png"
            r = requests.get(image_url, stream=True)
            r.raise_for_status()
        except requests.HTTPError:
            image_url = f"https://s3.eu-central-1.amazonaws.com/chemicalinventory-structures-frankfurt/ID-{self.compound_id}.png"
            r = requests.get(image_url, stream=True)
            r.raise_for_status()
        return r.raw.read()

    @property
    def name(self):
        '''Return the name of the container'''
        return self._name

    @property
    def location(self):
        '''Return a location object representing the location of the container'''
        return self._location

    # @location.setter
    # def location(self, location):
    #     if not location or location.isinstance(Location):
    #         self._location = location
    #     else: 
    #         raise TypeError('Assigned location must be a Location object.')

    @property
    def smiles(self):
        '''Return the smiles code of  the compound'''
        return self._smiles

    @property
    def size(self):
        '''Return the size of the container'''
        return self._size

    @property
    def comments(self):
        '''Return any comments on the container'''
        return self._comments

    @property
    def barcode(self):
        '''Return the barcode of the container'''
        return self._barcode

    @property
    def supplier(self):
        '''Return the supplier of the contianer'''
        return self._supplier

    @property
    def date_acquired(self):
        '''Return the date the container was acquired'''
        return self._date_acquired

    @property
    def owner(self):
        '''Return the name of the person who owns the container'''
        return self._owner

    @property
    def linked_files(self):
        '''Returned files linked to container'''
        return self._linked_files

class Location:
    def __init__(self, name, inventory_id=None, parent=None, group=None, barcode=None):
        self._inventory_id = inventory_id
        self._name = name
        # if not parent or parent.isinstance(Location):
        #     self._parent = parent
        # else: 
        #     raise TypeError('Assigned parent must be a Location object.')
        self._parent = parent
        self._group = group
        self._barcode = barcode

    def __repr__(self):
        return f"Location: {self.name}"

    def __eq__(self, other):
        
        return self.name == other.name

    @property
    def inventory_id(self):
        '''Return the inventory id of the location'''
        return self._inventory_id

    @property
    def name(self):
        '''Return the name of the location'''
        return self._name

    @property
    def parent(self):
        return self._parent

    # @parent.setter
    # def parent(self, parent):
    #     if not parent or parent.isinstance(Location):
    #         self._parent = parent
    #     else: 
    #         raise TypeError('Assigned parent must be a Location object.')

    @property
    def group(self):
        return self._group

    @property
    def barcode(self):
        return self._barcode


class Group:
    def __init__(self, name, inventory_id=None):
        self._name = name
        self._inventory_id = inventory_id

    def __repr__(self):
        return f"Group: {self.name}"

    def __eq__(self, other):
        return self.name==other.name or self.inventory_id==other.inventory_id

    @property
    def name(self):
        return self._name

    @property
    def inventory_id(self):
        return self._inventory_id

class Compound:
    def __init__(self, compound_id,
                 names=None, cas=None, smiles=None, 
                 molecular_formula=None, molecular_weight=None,
                 mass=None, ghs=None):
        self._compound_id = compound_id
        self._names = names
        self._cas = cas
        self._smiles = smiles
        self._molecular_formula = molecular_formula
        self._molecular_weight = molecular_weight
        self._mass = mass
        self._ghs = ghs


    def __repr__(self):
        return f"Compound {self._compound_id}: {self._names}, CAS {self._cas}"

    def __eq__(self, other):
        return isinstance(other, Compound) and self.compound_id == other.compound_id

    def _repr_png_(self):
        '''Return image for use in jupyter notebook'''
        return self.image

    @property
    def compound_id(self):
        '''Compound record ID'''
        return self._compound_id
                
    @property
    def names(self):
        '''Compound IUPAC names'''
        return self._names

    @property
    def cas(self):
        '''Compound CAS'''
        return self._cas

    @property
    def smiles(self):
        '''Compound SMILES'''
        return self._smiles

    @property
    def molecular_formula(self):
        '''Compound molecular formula'''
        return self._molecular_formula
    
    @property
    def molecular_weight(self):
        '''Compound molecular weight'''
        return self._molecular_weight

    @property
    def mass(self):
        '''Compound exact mass'''
        return self._mass

    @property
    def ghs(self):
        '''Compound GHS record'''
        return self._ghs
                
    @property
    def image(self):
        '''Return an image of the structure of the compound'''
        try:
            image_url = f"https://s3.eu-central-1.amazonaws.com/chemicalinventory-structures-frankfurt/ID-{self.compound_id}-1.png"
            r = requests.get(image_url, stream=True)
            r.raise_for_status()
        except requests.HTTPError:
            image_url = f"https://s3.eu-central-1.amazonaws.com/chemicalinventory-structures-frankfurt/ID-{self.compound_id}.png"
            r = requests.get(image_url, stream=True)
            r.raise_for_status()
        return r.raw.read()
