"""
plazi.py

This script is getting the information from the taxonomic treatments.

Search on Genus + species --> this will only give results of the treatments where the name is given like this. Synonyms are not showing up in this case.

the authority is contained in dwc:authority.

TO BE ADDED: I need to loop over all the synonyms in order to find all the relevant treatments!

"""

from SPARQLWrapper import SPARQLWrapper, JSON
import warnings
warnings.filterwarnings('ignore')
from rdflib import *
from urllib.request import urlopen
from urllib.error import HTTPError

plazi_base_url = 'http://tb.plazi.org/GgServer/rdf/'
plazi_sparql = 'https://treatment.ld.plazi.org/sparql'

def get_treatments(genus,species):

    p_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    PREFIX treat: <http://plazi.org/vocab/treatment#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    SELECT * WHERE {{ 
        ?tc dwc:genus "{0}" .
        ?tc dwc:species "{1}" .
        ?tc a <http://filteredpush.org/ontologies/oa/dwcFP#TaxonConcept> . 
    OPTIONAL {{ ?tc treat:hasTaxonName ?tn . }}
    OPTIONAL {{ ?augmentingTreatment treat:augmentsTaxonConcept ?tc . 
    ?augmentingTreatment dc:creator ?augmentingTreatmentCreator .}}
    OPTIONAL {{ ?definingTreatment treat:definesTaxonConcept ?tc . 
    ?definingTreatment dc:creator ?definingTreatmentCreator .}}
    }}

    """.format(genus,species)

    treatments = []

    sparql = SPARQLWrapper(plazi_sparql)
    sparql.setQuery(p_query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()


    for result in results["results"]["bindings"]:
        try:
            treatments.append(result['definingTreatment']['value'])
        except KeyError:
            pass
        try:
            treatments.append(result['augmentingTreatment']['value'])
        except KeyError:
            pass



    treatments = list(set(treatments))

    return treatments

def get_treatment_information(treatment):
    url = plazi_base_url + treatment.replace('http://treatment.plazi.org/id/','')
    g = Graph()

    try:
        g.parse(url, format='xml')
        # Get the publication

        publication_query = g.query(
         """ SELECT * WHERE {{
        <{0}> trt:publishedIn ?b.
        OPTIONAL{{ ?b dc:title ?title.}}
        OPTIONAL{{ ?b dc:creator ?creator.}}
        OPTIONAL{{ ?b bibo:journal ?journal.}}
        OPTIONAL{{ ?b dc:date ?date.}}
        OPTIONAL{{ ?b bibo:volume ?volume.}}
        }}""".format(treatment))

        pub_print = True

        publications = []

        figures = []

        type_string = []

        if pub_print:

            for item in publication_query:
                publication = {}
                publication['published in'] = item.b
                publication['author'] = item.creator
                try:
                    publication['title'] = item.title
                    publication['journal'] = item.journal
                    publication['date'] = item.date
                    publication['volume'] = item.volume
                except Exception:
                    publication['title'] = 'N/A'
                    publication['journal'] = 'N/A'
                    publication['date'] = 'N/A'
                    publication['volume'] = 'N/A'
                publications.append(publication)

        # Get the figures

        qfig = g.query(
        """ SELECT * WHERE {{
        <{0}> fabio:hasPart ?b.
        ?b rdf:type <http://purl.org/spar/fabio/Figure>.
        }}""".format(treatment))

        for fig in qfig:
          figures.append(fig[0])

        # Get the sections within the treatment
        qres = g.query(
          """ SELECT DISTINCT * WHERE {{
        <{0}> spm:hasInformation ?b.
        }}""".format(treatment))


        # For each section in the treatment, check if there is Type information

        for r in qres:
            q2res = g.query(
            """ SELECT DISTINCT * WHERE {{
             <{0}> spm:hasContent ?b.
             }}""".format(r[0]))

            for r2 in q2res:
                if str(r2).lower().find('type') != -1:
                    print('=================')
                    print('Type information:')
                    print('-----------------')
                    print(str(r2[0]))

                    type_string.append(r2[0].toPython())

        return publications, figures, type_string

    except HTTPError:

        print('treatment gave an HTTP error')
        return None,None,None

if __name__ == "__main__":
    import sys
    output = get_treatments(sys.argv[1],sys.argv[2])
    for treatment in output:
        print(treatment)
        p,f,t = get_treatment_information(treatment)
        print(t)
