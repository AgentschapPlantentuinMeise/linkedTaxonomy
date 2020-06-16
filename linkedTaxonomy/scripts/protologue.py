import requests
import json
import dateutil.parser as dparser

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

    date = None
    try:
        date = dparser.parse(type_string,fuzzy=True)
    except ValueError:
        date = None

    
    type_string = type_string.split()
    for substring in type_string:
        substring = substring.replace(',', '').replace('!', '').replace(')','').replace(';','').replace('.','').replace('(','').replace(' ','')
        if substring in IH_codes:
            collections.append(substring)


    return date, collections

def types_mentionned(string):

    types = ['holotype', 'isotype', 'paratype', 'syntype', 'lectotype', 'isolectotype', 'neotype', 'isoneotype', 'epitype']
    
    result = []

    for tstr in types:
        if string.lower().find(tstr) != -1:
            result.append(tstr)

    return result

if __name__ == '__main__':
    import sys
    date, collections = find_collections(sys.argv[1])
    tm = types_mentionned(sys.argv[1])

    print(tm)
