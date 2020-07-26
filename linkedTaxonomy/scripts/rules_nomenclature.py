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
    try:
        if len(df.scientificName) == len(df.scientificName.unique()):
            result = Evaluation.OK
    except AttributeError:
        result = Evaluation.TO_BE_CHECKED

    return result

def check_date_isotypes(name, date, df):

    result = Evaluation.OK
    message = ''
    date = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
    print(date)

    df = df[df.scientificName == name]

    if not df.empty:
        for isodate in df.eventDate:
            isodate_obj = datetime.strptime(isodate,'%Y-%m-%dT%H:%M:%S')
            if isodate_obj == date:
                result = Evaluation.OK
            elif isodate_obj.year == date.year:
                result = Evaluation.TO_BE_CHECKED
                message = 'Specimens are dating from the same year, please check'
            else:
                result = Evaluation.NOT_OK
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

        try:
            names = list_df[item].scientificName.tolist()
            if name in names:
                result[item] = Evaluation.NOT_OK
            else: 
                result[item] = Evaluation.OK
        except AttributeError:
            result[item] = Evaluation.TO_BE_CHECKED

    return result

def check_overlap_dates(dates1, dates2):

    status = Evaluation.OK

    dates2_obj = []
    for date in dates2:
        dates2_obj.append(datetime.strptime(date,'%Y-%m-%dT%H:%M:%S'))
    
    dset1 = set(dates1)
    intersect = dset1.intersection(dates2_obj)
    result_dates = list(intersect)

    if len(result_dates) == 0:
        status = Evaluation.TO_BE_CHECKED

    return status, result_dates


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



