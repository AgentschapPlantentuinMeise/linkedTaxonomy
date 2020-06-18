import protologue
import plazi
import type_specimen
import pandas as pd

def execute(genus,species):

    types = types_list = ['Holotype', 'Isotype',
            'Paratype', 'Syntype', 'Lectotype', 'Isolectotype',
            'Neotype', 'Isoneotype', 'Epitype', 'Type']

    taxonNameFull = genus + ' ' + species

    taxon = type_specimen.get_taxon_key(taxonNameFull)

    types_list = {}

    for item in types:
        types_list[item] = type_specimen.get_types(taxon['taxonKey'],item)

    treatments = plazi.get_treatments(genus,species)


    result = {}


    return result
