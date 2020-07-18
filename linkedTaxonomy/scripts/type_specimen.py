import requests
import json
import pandas as pd

import pykew.powo as powo
from pykew.powo_terms import Name
import pykew.ipni as ipni


# Base urls
gbif_base_url = 'https://api.gbif.org/v1/'
gbif_occurence = gbif_base_url + 'occurrence/search'
gbif_species = gbif_base_url + 'species/match' # to retrieve the taxonKey


def get_taxon_key(taxonNameFull):
    key = {}
    taxonKey_search = {'name' : taxonNameFull, 'strict' : True, 'verbose' : True}


    request = requests.get(gbif_species, params=taxonKey_search)

    if request.status_code == 200:
        req_json = json.loads(request.text)
        if req_json['matchType'] == 'NONE':
            return None

        key['taxonKey'] = req_json['usageKey']
        key['speciesKey'] = req_json['speciesKey']
        key['genusKey'] = req_json['genusKey']
        key['genus'] = req_json['genus']
        key['species'] = req_json['species'].split(' ')[1]

        return key

    else:
        return None



def get_types(key,type_status):

  type_search = {'taxonKey' : key, 'typeStatus' : type_status, 'limit' : 20}


  type_request = requests.get(gbif_occurence, params=type_search)
  if type_request.status_code == 200:
    types = json.loads(type_request.text)
    endOfRecords = types['endOfRecords']
    df = pd.DataFrame(types['results'])
    iteration = 1
    while not endOfRecords:
      type_search = {'taxonKey' : key, 'typeStatus' : type_status, 'limit' : 20, 'offset' : iteration*20}
      type_request = requests.get(gbif_occurence, params=type_search)
      types = json.loads(type_request.text)
      endOfRecords = types['endOfRecords']
      dfe = pd.DataFrame(types['results'])
      df = df.append(dfe, ignore_index=True)
      iteration += 1
  
    return df
  
  else:
    return None

def get_related_specimen(**kwargs):
    """
    input parameters expected:
    date
    genusKey or speciesKey
    recordedBy
    """
    query = {}
    for k,v in kwargs.items():
        query[k] = v
    query['limit'] = 20

    related = requests.get(gbif_occurence, params=query)
    if related.status_code == 200:
        related_specimen = json.loads(related.text)
        endOfRecords = related_specimen['endOfRecords']
        df = pd.DataFrame(related_specimen['results'])
        iteration = 1
        while not endOfRecords:
            query['offset'] =  iteration*20
            related = requests.get(gbif_occurence, params=query)
            related_specimen = json.loads(related.text)
            endOfRecords = related_specimen['endOfRecords']
            dfe = pd.DataFrame(related_specimen['results'])
            df = df.append(dfe, ignore_index=True)
            iteration += 1
  
        return df

    else:
        return None
  

def get_synonyms(genus,species):

    p_query = {Name.genus : genus, Name.species : species}

    name = []
    synonyms = []

    results = ipni.search(p_query)
    spec = []
    for r in results:
        if r['rank'] == 'spec.':
            spec.append(r)


    for s in spec:
        powo_result = powo.lookup(s['fqId'])
        try:
            for synonym in powo_result['synonyms']:
                synonyms.append(synonym)
        except KeyError:
            return None

    return synonyms

if __name__ == "__main__":
    import sys
    columns = ['key','scientificName', 'taxonRank']
    taxon = get_taxon_key(sys.argv[1])
    types = get_types(taxon['taxonKey'],sys.argv[2])

    print(types[columns])
