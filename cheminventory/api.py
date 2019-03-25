from .objects import Container, Location, Group
from .utils import flatten_list
import requests
import json, os, re


class ChemInventory:
    def __init__(self, email: str=None, password: str=None):
        self. email = str(os.environ.get('CHEMINVENTORY_EMAIL', email))
        self.password = str(os.environ.get('CHEMINVENTORY_PASS', password))
        self.jwt = None
        self._login(self.email, self.password)
        #I am assuming that first group in the list is always your group. 
        # Need to verify this
        locs = self._post('general-retrievelocations', 'locations')
        self.groupid = locs['groupinfo'][0]['id']
        self.userid = None

    def _post(self, path, referer_path: str, data: dict=None):
        url = "https://access.cheminventory.net/ajax/" + path + ".php"
        headers = {
                    'authority': "access.cheminventory.net",
                    'path': '/ajax' + path + ".php",
                    'origin': "https://access.cheminventory.net",
                    "accept-language": "en-US,en;q=0.9,es;q=0.8",
        }
        if referer_path:
            headers.update({'referer':f"https://access.cheminventory.net/{referer_path}.php"})
        if self.jwt:
            headers.update({'cookie': f"jwt={self.jwt}"})
        if data:
            r = requests.post(url, headers=headers, data=data)
        else:
            r = requests.post(url, headers=headers)
        r.raise_for_status()
        return json.loads(r.text)
    
    def _login(self, email: str, password: str):
        data={'email': email, 'pass': password}
        r = self._post('index-signin', 'home', data=data)
        self.jwt = r['jwt']
        return r

    def search(self, query, locations: list=None):
        '''Search using the CAS number, barcode or chemical name
        '''
        cas_number = re.search(r"\b[1-9]{1}[0-9]{1,5}-\d{2}-\d\b", str(query))
        if cas_number:
            query = cas_number[0]
            search_type = 'cas'   
        else:
            try:
                query = int(query)
                search_type = 'barcode'
            except ValueError:
                query = f"%{query}%"
                search_type = 'name'
        if not locations:
            locations = self.get_locations(filter_to_my_group=True)
            locations = [loc.inventory_id for loc in locations]
        data = {
            'groupid': self.groupid,
            'searchtype': search_type,
            'searchterm':  query,
            'limitlocations': locations.append(1)
        }
        r = self._post('search-search', referer_path='search', data=data)
        
        #return a list of container objects
        if r['searchresults']['containers']:
            containers = []
            for container in r['searchresults']['containers']:
                loc = Location(name=container.get('location'))
                ct = Container(
                    inventory_id = container.get('id'), 
                    compound_id = container.get('sid'),
                    name=container.get('containername'),
                    location=loc,
                    size=container.get('size'),
                    smiles=container.get('smiles'),
                    cas=container.get('cas'),
                    comments=container.get('comments'),
                    barcode=container.get('barcode'),
                    supplier=container.get('supplier'),
                    date_acquired=container.get('dateacquired'),
                    owner=container.get('owner'))
                containers.append(ct)
            return containers
        else:
            return []

    def add_container(self, ):
        raise NotImplementedError()

    def move_container(self, barcode, new_location):
        data = {
            'barcode': barcode,
            'containerid': 0,
            'locationid': 0,
            'userid': 0,
            'referral': 'search.php'
        }
        r = self._post('scantomove-process', 'search', data=data)
        if r['status'] == 'nomatch':
            raise ValueError(f"No container with the barcode {barcode} found")
        elif r['status'] == 'success':
            new_data = {
                'barcode': barcode,
                'containerid': r['data']['id'],
                'locationid': new_location.inventory_id,
                'userid': self.userid, 
                'referral': 'search.php' 
            }
            r = self._post('scantomove-process', 'search', data=new_data)
            if r['status'] == 'moved':
                pass
            else:
                raise ProcessLookupError("Not able to move container")
        
    def get_groups(self):
        '''Retrieve groups listed in ChemInventory'''
        resp = self._post('general-retrievelocations', 'locations')
        final_resp = []
        if resp['groupinfo']:
            for group in resp['groupinfo']:
                final_resp.append(Group(
                    name=group.get('name'),
                    inventory_id=group.get('id')
                ))
        return final_resp

    def get_locations(self, filter_to_my_group=False):
        """Retrieve Locations listed in ChemInventory"""
        resp = self._post('general-retrievelocations', 'locations')
        groups = {}
        if resp['groupinfo']:
            for group in resp['groupinfo']:
                groups[group['id']] = Group(
                                            name=group.get('name'),
                                            inventory_id=group.get('id')
                                            )
        final_resp = []
        if resp['data']:
            if filter_to_my_group:
                resp['data'] = {self.groupid: resp['data'][self.groupid]}
            for groupid, sublocation in resp['data'].items():
                if type(sublocation) is dict:
                    sublocation = [loc for _, loc in sublocation.items()]
                    sublocation = flatten_list(sublocation)
                if type(sublocation) is list:
                    sublocation = flatten_list(sublocation)
                for location in sublocation:
                    group = groups[groupid]
                    final_resp.append(Location(
                                            name=location.get('name'),
                                            inventory_id=location.get('id'),
                                            parent=location.get('parent'),
                                            group=group,
                                            barcode=location.get('barcode')
                                      ))
        return final_resp
    
    def get_containers(self, include_only=[]):
        """Download all the containers owned by a group

        Arguments
        ---------
        include_only: List containg `Group` or `Location` objects
            Search only over a list of groups or locations         
        """
        locations = self.get_locations() 
        if len(locations) == 0:
            raise ValueError("No locations for containers exist in Cheminventory")

        final_locations = []
        if include_only:
            for location in locations:
                check = location in include_only or location.group in include_only
                if check:
                    final_locations.append(location)
            if len(final_locations)==0: raise ValueError(f"Location(s) or group(s) {include_only} is/are not in the database.")
        else:
            final_locations = locations

        containers = []
        for location in final_locations:
            containers += self._get_location_containers(location.inventory_id)

        return containers

    def _get_location_containers(self, location_id):
        resp = self._post('locations-getcontainers', 'locations', data={'location': location_id})
        containers = []
        for container in resp['results']:
            loc = Location(container.get('location'))
            ct = Container(
                    inventory_id = container.get('id'), 
                    compound_id = container.get('sid'),
                    name=container.get('containername'),
                    location=loc,
                    size=container.get('size'),
                    smiles=container.get('smiles'),
                    cas=container.get('cas'),
                    comments=container.get('comments'),
                    barcode=container.get('barcode'),
                    supplier=container.get('supplier'),
                    date_acquired=container.get('dateacquired'),
                    owner=container.get('owner'))
            containers.append(ct)
        return containers
        

