# Linking nomenclature to specimens
## Introduction
All known species receive a name. 

When a name is given to a specimen...
## Methodology
### Getting all the building blocks
In order to reconstruct the information on a scientific name, we use the different available APSs
* GBIF API: type specimens and related specimens
* PLAZI SPARQL endpoint: retreive information on the scientific name out of the protologue, get the collection identifiers
* Index Herbariorum: from the collection identifiers, look for the collections mentioned in the protologue
### Workflow
* based on the taxon name, look for the taxon key in GBIF
* search for all type specimen that belong to the same taxon
* look for that taxon on Plazi and find the treatments 
* parse the type information in the treatment + year/date of treatment
* apply rules of nomenclature

### Rules of nomenclature
* For each name only one holotype
* isotypes same date

### Visualisation

## Recommendations
### Unique identifiers for collections
In order to find the holding collecion of the type specimen, Index Herbariorum needs to be used. The letter code is unique for herbaria, but not for collections
* GrSciColl recommendations

## Structure of the repository

The code is written in Python 3. Please use version 3.6 or higher.

The repository contains two main folders. The 'notebooks' folder is a selection of Jupyter notebooks that were used to explore the possibilities with the different APIs and how this information can be extracted.

The real code is contained in the 'linkedTaxonomy' folder. This folder contains a python Flask application. The application takes Genus and epithet as input to run the checks on nomenclature and build the information known on this taxon. A timeline is built to show the history of this taxon.

```bash
|-- requirements.txt
|-- LICENSE.txt
|-- README.md
|-- notebooks
    |-- Name_information_types.ipynb
    |-- Types_GBIFonly.ipynb
    |-- Wikidata_taxon.ipynb
|-- linkedTaxonomy
    |-- app.py
    |-- scripts
        |-- bhl_results.py
        |-- index.py
        |-- lt_html.py
        |-- plazi.py
        |-- protologue.py
        |-- rules_nomenclature.py
        |-- type_specimen.py
        |-- wikidata.py
    |-- templates
        |-- home.html
        |-- taxon.html
 ```

In order to start the application, run `app.py`. This will start a development server running on your localhost. In order to deploy this application, you should setup a WSGI interface and a server (e.g. Apache)

## References
To be added
