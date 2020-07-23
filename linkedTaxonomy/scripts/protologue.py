"""
protologue.py

This part of the code is parsing the information in the treatments to find date of the specimen, the types mentioned in the treatment and the collections that contain the specimen

The date returned by the script is possibly a list of possible dates. Extra logic needs to be put in place to make sure that unrealistic dates are rejected.

"""

import requests
import json
import datefinder
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

    # TO DO: improve the parsing of the type string
    # some parts of the string are recognized as collection
    # codes, while this shouldn´t be the case

    collections = []

    date = None
    try:
        date = list(datefinder.find_dates(type_string))
    except ValueError:
        date = None
    except TypeError:
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

    print(date)
    print(tm)
