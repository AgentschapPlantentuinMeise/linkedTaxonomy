import protologue
import plazi
import type_specimen
import pandas as pd

def check_unique_holotype(df):

    result = False
    if len(df.scientificName) == len(df.scientificName.unique():
            result = True

    return result

def check_date_isotypes(name,date,df):

    result = False
    df = df[df.scientificName == name]
    if not df.isempty:
        for isodate in df.eventDate:
            if isodate == date:
                result = True

    return result
    


def execute(genus,species):

    status = 'OK'
    
    types = types_list = ['Holotype', 'Isotype',
            'Paratype', 'Syntype', 'Lectotype', 'Isolectotype',
            'Neotype', 'Isoneotype', 'Epitype', 'Type']

    taxonNameFull = genus + ' ' + species

    taxon = type_specimen.get_taxon_key(taxonNameFull)

    types_list = {}

    for item in types:
        types_list[item] = type_specimen.get_types(taxon['taxonKey'],item)

    # treatments = plazi.get_treatments(genus,species)
    # lets not focus on the treatments yet

    result = types_list


    return status, result
