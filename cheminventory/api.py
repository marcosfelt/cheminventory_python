import requests
import pandas
from contextlib import closing
import codecs, io, json, os, sys, re
from .utils import flatten_list

class ChemInventory:
    def __init__(self, email, password):
        self. email = email
        self.password = password
        self.jwt = None
        self._login(email, password)
        #I am assuming that first group is the list is always your group. 
        # Need to verify this
        locs = self.retrieve_locations()
        self.groupid = locs['groupinfo'][0]['id']

    def _post(self, path, referer_path, data=None):
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
    
    def _login(self, email, password):
        data={'email': email, 'pass': password}
        r = self._post('index-signin', 'home', data=data)
        self.jwt = r['jwt']

    def search(self, query, locations=None):
        '''Search using the CAS number, barcode or chemical name
        '''
        cas_number = re.search('\b[1-9]{1}[0-9]{1,5}-\d{2}-\d\b', query)
        if cas_number:
            query = cas_number[0]
            search_type = 'cas'
        elif query is int:
            search_type = 'barcode'
        else:
            query = f"%{query}%"
            search_type = 'name'
        if not locations:
            locations = self.retrieve_locations(filter_to_my_group=True)
            locations = [loc['id'] for loc in locations]
        data = {
            'groupid': self.groupid,
            'searchtype': search_type,
            'searchterm':  query,
            'limitlocations': locations.append(1)
        }
        
        r = self._post('search-search', referer_path='search', data=data)
        return r['searchresults']['containers']

    def add_container(self):

        raise NotImplementedError()

    def move_containers(self):
        raise NotImplementedError()

        
    def retrieve_locations(self, filter_to_my_group=False):
        """Retrieve Locations listed in ChemInventory"""
        resp = self._post('general-retrievelocations', 'locations')
        if filter_to_my_group:
            resp = flatten_list(resp['data'][self.groupid])
        return resp
    
    def download_location_containers(self, location: str, file_path=''):
        """Download a csv file with all containers in a location"""
        loc_data = self.retrieve_locations()
        loc_id = None
        for loc in loc_data['groupinfo']:
            if loc['name'] == location:
                loc_id = loc['id']
            else:
                continue
        if not loc_id: raise ValueError(f"Location {location} is not in the database.")
        
        cupboard_list = flatten_list(list(loc_data['data'][loc_id]))

        df = None
        for cupboard in cupboard_list:
            cupboard_data = self._download_cupboard_data(cupboard['id'], file_path)
            try:
                df = df.append(cupboard_data, ignore_index=True)
            except AttributeError:
                df = cupboard_data
        if file_path:
            file_path = f"{file_path.rstrip('.csv')}.csv"
            df.to_csv(file_path, index=False)
        return df

    def _download_cupboard_data(self, cupboard_id, file_path=''):
        containers = self._post('locations-getcontainers', 'locations', data={'location': cupboard_id})
        df = pandas.DataFrame(containers['results'])
        return df
        

