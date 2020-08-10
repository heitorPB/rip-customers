import os

from dotenv import load_dotenv
import requests

load_dotenv('settings.env')
MAP_KEY = os.getenv('MAP_KEY')


def coordinates(search: str) -> dict:
    """Return the coordinates of a geo search"""

    url = f'https://www.mapquestapi.com/geocoding/v1/address?key={MAP_KEY}' \
          f'&inFormat=kvp&outFormat=json&location={search}&thumbMaps=false'

    r = requests.get(url)

    coordinates = {'latitude': '',
                   'longitude': ''}

    if r.ok:
        coords = r.json()['results'][0]['locations'][0]['latLng']
        coordinates['latitude'] = coords['lat']
        coordinates['longitude'] = coords['lng']

    return coordinates
