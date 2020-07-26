import sys
sys.path.append('./scripts/')

from flask import render_template

from flask import Flask, url_for
from flask import Response, make_response
from markupsafe import escape
from datetime import date
import wikidata
import plazi
import lt_html
import html
import protologue
import type_specimen
import index
import rules_nomenclature

import base64
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home(table=None):
    df = wikidata.list_wd()
    print(df.to_html(classes='data', header='true', max_rows=10))
    return render_template('home.html', tables=[df.to_html(classes='data', header=True, index=False, escape=False)])

@app.route('/<genus>/<species>')
def taxon(genus=None, species=None):

    # list of types to consider
    types = ['Holotype', 'Isotype', 
            'Paratype', 'Syntype', 'Lectotype', 'Isolectotype', 
            'Neotype', 'Isoneotype', 'Epitype', 'Type']
    
    # get information from GBIF
    taxonNameFull = genus + ' ' + species
    print('Debug info')
    print(taxonNameFull)
    taxon = type_specimen.get_taxon_key(taxonNameFull)
    print(taxon)
    # get all the type specimen
    try:
        status, types_list = rules_nomenclature.get_specimen(genus, species)
    except TypeError:
        types_list = None

    # create tables for the specimen
    if types_list is not None:
        holotype_table = lt_html.make_specimen_table(types_list['Holotype'])
        isotype_table = lt_html.make_specimen_table(types_list['Isotype'])
        paratype_table = lt_html.make_specimen_table(types_list['Paratype'])
        syntype_table = lt_html.make_specimen_table(types_list['Syntype'])
        lectotype_table = lt_html.make_specimen_table(types_list['Lectotype'])
        isolectotype_table = lt_html.make_specimen_table(types_list['Isolectotype'])
        neotype_table = lt_html.make_specimen_table(types_list['Neotype'])
        isoneotype_table = lt_html.make_specimen_table(types_list['Isoneotype'])
        epitype_table = lt_html.make_specimen_table(types_list['Epitype'])
        type_table = lt_html.make_specimen_table(types_list['Type'])

    
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
    dates_tot = []
    collections_tot = []

    for treatment in treatments:
        p,f,t = plazi.get_treatment_information(treatment)
        if f is not None:
            images.extend(f)
        if p is not None:
            publications.extend(p)
        if t is not None:
            type_information.extend(t)

    treatmentsHaveLectotype = False

    image_list = lt_html.include_images(images)
    for item in type_information:
        if 'lectotype' in item.lower():
            treatmentsHaveLectotype = True
        date_p, collections_p = protologue.find_collections(item)
        dates_list = []
        try:
            for date in date_p:
                if date.year > 1000 and date < date.today():
                    dates_list.append(date)
        except TypeError:
            dates_list = []

        dates_tot.extend(dates_list)
        collections_tot.extend(collections_p)

    cdf = index.get_collectionsList(set(collections_tot))
    collections_table = cdf.to_html(classes='data', header=True, index=False, escape=False)

    
    if treatmentsHaveLectotype:
        
        type_numbers = {}
        type_numbers['Holotype'] = len(types_list['Holotype'])
        type_numbers['Isotype'] = len(types_list['Isotype'])
        type_numbers['Lectotype'] = len(types_list['Lectotype'])
        type_numbers['Paratype'] = len(types_list['Paratype'])
        type_numbers['Type'] = len(types_list['Type'])

        # If Holotypes exist for names, plot the holotypes
        fig = type_specimen.plot_timeline(types_list['Holotype'])
        pngImage = BytesIO()
        if fig is not None:
            fig.savefig(pngImage, format='png')

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        else:
            pngImageB64String = None

        
        # checks on nomenclature
        rules_check = {}
        rules_check['Unique Holotype per name'] = rules_nomenclature.check_unique_holotype(types_list['Holotype'])
        for name in types_list['Lectotype'].scientificName:
            rule = rules_nomenclature.check_lectotype(name, types_list)
            for t,r in rule.items():
                check_str = 'No ' + t + ' for name: ' + name
                rules_check[check_str] = r
        if len(types_list['Isotype']) > 0:
                for name in types_list['Holotype'].scientificName:
                    check_str = 'Isotypes of ' + name + ' have the same date'
                    for i, row in types_list['Holotype'].iterrows():
                        if row.scientificName == name:
                            try:
                                date = row.eventDate
                                result, message = rules_nomenclature.check_date_isotypes(name, date, types_list['Isotype'])
                                rules_check[check_str] = result
                            except Exception:
                                rules_check[check_str] = "Evaluation.TO_BE_CHECKED"

        print(rules_check)


        return render_template('taxon.html', genus=genus, species=species, timeline=pngImageB64String, type_numbers=type_numbers, synonyms=synonyms, treatments=treatments, image_list=image_list, type_information=type_information, collections_table=[collections_table], rules=rules_check, holotype_table=[holotype_table], isotype_table=[isotype_table], paratype_table=[paratype_table], neotype_table=[neotype_table], lectotype_table=[lectotype_table], type_table=[type_table])

    
    else:
        
        type_numbers = {}
        type_numbers['Holotype'] = len(types_list['Holotype'])
        type_numbers['Isotype'] = len(types_list['Isotype'])
        type_numbers['Lectotype'] = len(types_list['Lectotype'])
        type_numbers['Paratype'] = len(types_list['Paratype'])
        type_numbers['Type'] = len(types_list['Type'])

       
        # plot the timeline of holotypes
        fig = type_specimen.plot_timeline(types_list['Holotype'])
        pngImage = BytesIO()
        if fig is not None:
            fig.savefig(pngImage, format='png')

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        else:
            pngImageB64String = "placeholder"

        # checks on nomenclature
        rules_check = {}
        rules_check['Unique Holotype per name'] = rules_nomenclature.check_unique_holotype(types_list['Holotype'])
        if len(types_list['Isotype']) > 0:
                for name in types_list['Holotype'].scientificName:
                    check_str = 'Isotypes of ' + name + ' have the same date'
                    for i, row in types_list['Holotype'].iterrows():
                        if row.scientificName == name:
                            try:
                                date = row.eventDate
                                result, message = rules_nomenclature.check_date_isotypes(name, date, types_list['Isotype'])
                                rules_check[check_str] = result
                            except Exception:
                                rules_check[check_str] = "Evaluation.TO_BE_CHECKED"
        
        
        return render_template('taxon.html', genus=genus, species=species, timeline=pngImageB64String, type_numbers=type_numbers, synonyms=synonyms, treatments=treatments, image_list=image_list, type_information=type_information, rules=rules_check, collections_table=[collections_table], holotype_table=[holotype_table], isotype_table=[isotype_table], paratype_table=[paratype_table], neotype_table=[neotype_table], lectotype_table=[lectotype_table], type_table=[type_table])



if __name__ == '__main__':

    app.run(port=5000,debug=True)
