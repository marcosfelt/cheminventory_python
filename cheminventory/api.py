from requests import Session
import requests
import json
from contextlib import closing
import codecs
import csv

class ChemInventory:
    def __init__(self, email, password):
        self. email = email
        self.password = password
        self.jwt = None
        self._login(email, password)

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
        
    def retrieve_locations(self):
        """Retrieve Locations listed in ChemInventory"""
        resp = self._post('general-retrievelocations', 'locations')
        return resp
    
    def download_location_containers(self, location: str, file_name=None):
        """Download a csv file with all containers in a location"""
        loc_data = self.retrieve_locations()
        loc_id = None
        for loc in loc_data['groupinfo']:
            if loc['name'] == location:
                loc_id = loc['id']
            else:
                continue
        if not loc_id: raise ValueError(f"Location {location} is not in the database.")

        if loc_data['data'][loc_id] is list:
            cupboard_list = loc_data['data'][loc_id]
        else:
            my_lists = loc_data['data'][loc_id]
            cupboard_list = []
            for el in my_lists:
                cupboard_list += el

        if file_name:
            path = f"{file_name.rstrip('.csv')}.csv"

        for cupboard in cupboard_list:
            csv_output = self._download_cupboard_data(cupboard['id'], path)
            yield csv_output

    def _download_cupboard_data(self, cupboard_id, file_path=None):
        containers = self._post('locations-getcontainers', 'locations', data={'location': cupboard_id})
        container_ids = [container['id'] for container in containers['results']]
        resp = self._post('general-exportbycontainerid', 'locations', data = {'container_ids': container_ids})
        link = resp['link']
        csv_output = None
        if file_path:
            csv_output = self._download_csv(link, csv_output, file_path)
        else:
            csv_output = self._download_csv(link, csv_output)
        return csv_output

    def _download_csv(self, link, save_path=None):
        headers = {
            "Host": "chemicalinventory-generatedfiles.s3.eu-west-1.amazonaws.com",
            "Referer": "https://access.cheminventory.net/locations.php",
            'cookie': f"jwt={self.jwt}"
        } 
        csv_output = None
        with closing(requests.get(link, headers=headers, stream=True)) as r:
            r.raise_for_status()
            l = r.iter_lines()
            if save_path:
                with open(save_path, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(l)
            csv_output = csv.reader(l)
        return csv_output
        
    def search(self, query):
        raise NotImplementedError()
        return

    def add_container(self):
        raise NotImplementedError()

    def move_containers(self):
        raise NotImplementedError()
    