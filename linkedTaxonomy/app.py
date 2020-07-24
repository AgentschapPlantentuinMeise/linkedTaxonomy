import sys
sys.path.append('./scripts/')

from flask import render_template

from flask import Flask, url_for
from markupsafe import escape
import wikidata
import plazi
import lt_html
import html
import protologue
import type_specimen
import index

import base64
from io import BytesIO
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/')
def home(table=None):
    df = wikidata.list_wd()
    print(df.to_html(classes='data', header='true', max_rows=10))
    return render_template('home.html', tables=[df.to_html(classes='data', header=True, index=False, escape=False)])

@app.route('/<genus>/<species>')
def taxon(genus=None, species=None):

    # list of types to consider
    types = types_list = ['Holotype', 'Isotype', 
            'Paratype', 'Syntype', 'Lectotype', 'Isolectotype', 
            'Neotype', 'Isoneotype', 'Epitype', 'Type']
    
    # get information from GBIF
    taxonNameFull = genus + ' ' + species
    print('Debug info')
    print(taxonNameFull)
    taxon = type_specimen.get_taxon_key(taxonNameFull)
    print(taxon)
    # get all the type specimen
    # Holotypes
    try:
        holotypes = type_specimen.get_types(taxon['taxonKey'],'Holotype')
        print(holotypes)
    except TypeError:
        holotypes = None
        print('No Holotype found')

    # Isotypes
    try:
        isotypes = type_specimen.get_types(taxon['taxonKey'],'Isotype')
    except TypeError:
        isotypes = None

    # Paratypes
    try:
        paratypes = type_specimen.get_types(taxon['taxonKey'],'Paratype')
    except TypeError:
        paratypes = None

    # Syntypes
    try:
        syntypes = type_specimen.get_types(taxon['taxonKey'],'Syntype')
    except TypeError:
        syntypes = None

    # Lectotypes
    try:
        lectotypes = type_specimen.get_types(taxon['taxonKey'],'Lectotype')
    except TypeError:
        lectotypes = None

    # Isolectotypes
    try:
        isolectotypes = type_specimen.get_types(taxon['taxonKey'],'Isolectotype')
    except TypeError:
        isolectotypes = None

    # Neotypes
    try:
        neotypes = type_specimen.get_types(taxon['taxonKey'],'Neotype')
    except TypeError:
        neotypes = None
    
    # Isoneotypes
    try:
        isoneotypes = type_specimen.get_types(taxon['taxonKey'],'Isoneotype')
    except TypeError:
        isoneotypes = None
    
    # Epitypes
    try:
        epitypes = type_specimen.get_types(taxon['taxonKey'],'Epitype')
    except TypeError:
        epitypes = None
   
    # Types
    try:
        types = type_specimen.get_types(taxon['taxonKey'],'Type')
    except TypeError:
        types = None
    
    
    # get synonyms
    synonyms = type_specimen.get_synonyms(genus,species)
    
    
    # get information from PLAZI
    treatments = plazi.get_treatments(genus,species)

    if synonyms is not None:
        for synonym in synonyms:
            genus_syn = synonym['name'].split(' ')[0]
            species_syn = synonym['name'].split(' ')[1]
            treatments_syn = plazi.get_treatments(genus_syn,species_syn)
            for st in treatments_syn:
                treatments.append(st)

    # Only use unique treatments
    treatments = set(treatments)


    images = []
    publications = []
    type_information = []

    for treatment in treatments:
        p,f,t = plazi.get_treatment_information(treatment)
        if f is not None:
            images.extend(f)
        if p is not None:
            publications.extend(p)
        if t is not None:
            type_information.extend(t)


    image_list = lt_html.include_images(images)
    for item in type_information:
        date_p, collections_p = protologue.find_collections(item)
        print(date_p)
        print(collections_p)
    
    if holotypes is not None:

        type_numbers = {}
        type_numbers['Holotype'] = len(holotypes)
        type_numbers['Isotype'] = len(isotypes)
        type_numbers['Lectotype'] = len(lectotypes)
        type_numbers['Paratype'] = len(paratypes)
        
        # create timeline of holotypes
        plot = type_specimen.plot_timeline(holotypes)
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        # checks on nomenclature
        rules_check = {}
        
        return render_template('taxon.html', genus=genus, species=species, data=data, type_numbers=type_numbers, synonyms=synonyms, image_list=image_list)


if __name__ == '__main__':

    app.run(port=5000,debug=True)
