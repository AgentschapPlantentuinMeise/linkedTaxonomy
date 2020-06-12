import requests
import json

IH_codes = []
herbaria = requests.get('http://sweetgum.nybg.org/science/api/v1/institutions')
if herbaria.status_code == 200:
  jHerb = herbaria.json()
  for element in jHerb['data']:
    IH_codes.append(element['code'])
else:
  print('Error reading IH API')



def find_collections(type_string):

    collections = []
    
    type_string = type_string.split()
    for substring in type_string:
        substring = substring.replace(',', '').replace('!', '').replace(')','').replace(';','').replace('.','').replace('(','').replace(' ','')
        if substring in IH_codes:
            collections.append(substring)


    return collections
