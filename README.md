# Linking nomenclature to specimens
Maarten Trekels - Meise Botanic Garden

## Introduction
When an organism is described for the first time, it will receive a scientific name. However, scientific knowledge is evolving continuously. Organisms with different names turn out to be the same and are merged into one species. Others turn out to be more diverse than first thought and are split into different species. When all of this pieces of the puzzle are put together, we speak about a taxon.

It is important to notice that this is a dynamic puzzle. Every day science finds new insights in the way nature works. How we understand a taxon today can be different from what it was yesterday and how it will be tomorrow. 

Crucial in the concept of a taxon are the different specimens that served as type material in the description of a scientific name. In order to have a full overview on the taxon, it is important to consider all these specimens in relation with the treatment in which they are described.

When specimens are added to GBIF, it is possible to indicate whether a specimen is a type specimen or not. Sometimes this information is incomplete (e.g. not specified what kind of type), missing or even wrong. Therefor, we implemented a number of checks on the rules of nomenclature in order to indicate possible issues with the specimens.

In this package of scripts, we focus on botanical specimens and treatments. However the principles can be expanded to any kind of organism. 


## Methodology
### Getting all the building blocks
In order to reconstruct the information on a scientific name, we use the different available APIs
* GBIF API: type specimens and related specimens
* PLAZI SPARQL endpoint: retreive information on the scientific name out of the protologue, get the collection identifiers
* Index Herbariorum: from the collection identifiers, look for the collections mentioned in the protologue
* IPNI/POWO: look for synonyms

### Workflow
![Design diagram](./linkedTaxonomy.jpg)

* based on the taxon name, look for the taxon key in GBIF
* search for all type specimen that belong to the same taxon
* look for that taxon on Plazi and find the treatments 
* parse the type information in the treatment + year/date of treatment
* apply rules of nomenclature
TO DO: describe time evolution. This should be taken in consideration, since names are given at different times.

### Rules of nomenclature
The rules of nomenclature are defined in `scripts\rules_nomenclature.py`. In this version of the application, the focus is solely on botany. This is the first set of functions to be adapted when expanding to other branches of biology.

The current rules that are implemented are:
* For each name only one holotype
* TO DO: if date of treatment known: check date specimen (only possible with defining treatments)
* isotypes same date
* check dates of the paratypes (less than or equal)
* if there is a lectotype: some types should not exist
* lectotype should be existing at the time of first description (rule to be defined)
* look for related specimen. 


### Visualisation
The set of scripts that implement the functionalities are serving a Python Flask web application. The only parameters that need to be given to the application are the Genus and epithet. A html page is generated from the different scripts. The specimens and treatments are shown (with pictures if available). As well as a table with the checks on nomenclaturial rules.

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
