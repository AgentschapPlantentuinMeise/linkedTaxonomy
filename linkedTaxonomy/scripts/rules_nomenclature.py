import protologue
import plazi
import type_specimen
import pandas as pd
from datetime import datetime
from enum import Enum

types = ['Holotype', 'Isotype', 
        'Paratype', 'Syntype', 'Lectotype', 'Isolectotype', 
        'Neotype', 'Isoneotype', 'Epitype', 'Type']

class Evaluation(Enum):
    OK = 0
    NOT_OK = 1
    TO_BE_CHECKED = 2


def check_unique_holotype(df):

    result = Evaluation.NOT_OK
    if len(df.scientificName) == len(df.scientificName.unique()):
            result = Evaluation.OK

    return result

def check_date_isotypes(name, date, df):

    result = Evaluation.OK
    message = ''

    df = df[df.scientificName == name]

    if not df.empty:
        for isodate in df.eventDate:
            isodate_obj = datetime.strptime(isodate,'%Y-%m-%dT%H:%M:%S')
            if isodate != date:
                result = Evaluation.NOT_OK
            elif isodate.year == date.year:
                result = Evaluation.TO_BE_CHECKED
                message = 'Specimens are dating from the same year, please check'
    else:
        result = Evaluation.TO_BE_CHECKED
        message = 'No information on isotypes of this name'

    return result, message
    
def check_date_paratypes(name, date, df):

    result = Evaluation.OK
    message = ''

    df = df[df.scientificName == name]

    if not df.empty:
        for paradate in df.eventDate:
            paradate_obj = datetime.strptime(paradate,'%Y-%m-%dT%H:%M:%S')
            if paradate_obj > date:
                result = Evaluation.NOT_OK
    else:
        result = Evaluation.TO_BE_CHECKED

    return result

def check_lectotype(name, list_df):

    result = {}

    rejected_types = ['Holotype', 'Isotype', 
            'Syntype', 'Neotype', 'Isoneotype', 'Epitype']

    for item in rejected_types:

        df = list_df[item]
        df = df[df.scientificName == name]
        if not df.empty:
            result[item] = Evaluation.NOT_OK
        else: 
            result[item] = Evaluation.OK

    return result


def get_specimen(genus,species):

    status = Evaluation.OK
    
    global types

    taxonNameFull = genus + ' ' + species

    taxon = type_specimen.get_taxon_key(taxonNameFull)

    types_list = {}

    for item in types:
        types_list[item] = type_specimen.get_types(taxon['taxonKey'],item)


    result = types_list


    return status, result



