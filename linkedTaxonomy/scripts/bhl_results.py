import os
import requests
import json

# defining variables
# bhl key should be stored in the environment variables

# description of BHL API: https://www.biodiversitylibrary.org/docs/api3.html
API_BHL = os.environ.get('BHL_KEY')
bhl_api = 'https://www.biodiversitylibrary.org/api3'


def get_bhl_info(genus,species):

    name = genus + '+' + species
    params = {'op':'PublicationSearch', 'searchterm' : name, 'searchtype': 'C',
            'apikey' : API_BHL , 'format' : 'json'}

    request = requests.get(bhl_api, params=params)


    if request.status_code == 200:
        result = json.loads(request.content)
        result = result["Result"]

    else:
        result = None

    return result

def bhl_scname_search(genus,species):

    name = genus + '+' + species
    params = {'op' : 'NameSearch' , 'name' : name, 'apikey' : API_BHL, 'format' : 'json'}

    
    request = requests.get(bhl_api, params=params)


    if request.status_code == 200:
        result = json.loads(request.content)
        result = result["Result"]

    else:
        result = None

    return result


if __name__ == '__main__':
    import sys
    output = globals()[sys.argv[1]](sys.argv[2],sys.argv[3])
    print(output)
