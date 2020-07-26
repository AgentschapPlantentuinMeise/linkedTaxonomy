# Linking nomenclature to type specimens
Maarten Trekels - Meise Botanic Garden

## Introduction
When an organism is formally described for the first time, it will receive a scientific Latin name. However, scientific knowledge is evolving continuously. Organisms with different names turn out to be the same and are merged into one species. Others turn out to be more diverse than first thought and are split into different species. When all of these pieces of the puzzle are put together, we speak about a taxon.

It is important to notice that this is a dynamic puzzle. Every day science finds new insights in the way nature works. How we understand a taxon today can be different from what it was yesterday and how it will be tomorrow. 

Crucial in the concept of a taxon are the different specimens that served as type material in the description of a scientific name. In order to have a full overview on the taxon, it is important to consider all these specimens in relation to the treatment in which they are described.

When specimens are added to the Global Biodiversity Information Facility (GBIF), it is possible to indicate whether a specimen is a type specimen or not. Sometimes this information is incomplete (e.g. not specifing what kind of type it is), missing or even wrong. Therefore, we have implemented a number of checks on the rules of nomenclature in order to indicate possible issues with these specimens.

In this package of scripts, we focus on botanical specimens and treatments. However the principles can be expanded to any kind of organism where the codes of nomenclature require a type specimen.


## Methodology
### Getting all the building blocks
In order to reconstruct the information on a scientific name, we use the different available APIs
* GBIF API: nomeclatural type specimens and other related specimens
* PLAZI SPARQL endpoint: to retreive information on the scientific name from the protologue, get the collection identifiers
* Index Herbariorum: from the collection identifiers, look for the collections mentioned in the protologue
* IPNI/POWO: to look for synonyms

### Workflow
![Design diagram](./linkedTaxonomy.jpg)

The application expects, as an input, the taxon name (genus + epithet). Based on those two parameters, a number of steps gather the information:

#### Step 1: search for the type specimen in GBIF

Using the genus and epithet, the application looks for the taxon key using the GBIF API (GBIF taxonomic backbone). Based on the taxon key, all type specimen with that key are retreived. Since the first version of this application is focussing on the botanical use-case, only 'Holotype', 'Isotype', 'Paratype', 'Syntype', 'Lectotype', 'Isolectotype', 'Neotype', 'Isoneotype', 'Epitype' and 'Type' are considered as type status.

By plotting the holotype specimens on a timeline, it is possible to display the time evolution of the species naming.

#### Step 2: get information from the treatments

The SPARQL endpoint of the Plazi Treatment Bank allows searching on dwc:genus and dwc:species (i.e. the epithet). As a result from the query, the defining and augmenting treatments can be retrieved. Using the persistent identifier of the treatment, a request can be performed to get the content of the treatment.
From this, the date of publication can be retrieved. By parsing the paragraph of the treatment that refers to the type specimens, the holding collections can be found (using the Index Herbariorum API).

#### Step 3: nomenclatural rules

* apply rules of nomenclature
TO DO: describe time evolution. This should be taken in consideration, since names are given at different times.

### Rules of nomenclature
The rules of nomenclature are defined in `scripts\rules_nomenclature.py`. In this version of the application, the focus is solely on botany. This is the first set of functions to be adapted when expanding to other branches of biology.

The current rules that are implemented are:
* For each name there should be only one holotype
* TO DO: if date of treatment known: check date specimen (only possible with defining treatments)
* isotypes should have the same date
* check dates of the paratypes (less than or equal)
* if there is a lectotype: neither a holotype nor neotype should exist
* lectotype should exist at the time of first description (rule to be defined)
* look for related specimens. 


### Visualisation
The set of scripts that implement the functionalities serve a Python Flask web application. The only parameters that need to be given to the application are the Genus and epithet. An html page is generated from the different scripts. The specimens and treatments are shown (with pictures if available). As well as a table with the checks on the nomenclatural rules.

## Recommendations
### Unique identifiers for collections
In order to find the holding collection of the type specimen, Index Herbariorum needs to be used. The letter code is unique for herbaria, but not for collections. In order to extend the application beyond botany, a unique identifier for each collection is needed. These unique identifiers should be linked to the relevant type specimens and treatments.
In order to have a better interlinking between them, these unique identifiers (e.g. GrSciColl identifiers) should be used by the scientist to refer to collections.

### Enrichment of collections data
This application is a demonstration on how collection data can be enriched with information on the different taxa. By linking type specimens to names and treatments, a more complete overview on a taxon is created.
Some relative easy ways to enrich the data are:
* collections could link type specimens to the relevant Plazi IDs
* linking the name under which a specimen is filed with a taxonomic ID (GBIF taxonKey or IPNI ID)

### Discovering hidden treasures
The application is demonstrating the power of discovering (possible) mistakes in the naming of specimen (by implementing a few simple nomenclatural rules). Apart from that, some type specimens are not flagged as being a type. As such, they are missing in the complete overview of a taxon. By looking at specimens that are possibly related to already known type specimen, it is possible to discover type specimens in the collections. 


### Special cases discovered
When testing the scripts, a special case was discovered. For 'Fallopia japonica' and 'Reynoutria japonica' (synonyms), the `genusKey` and `speciesKey` are the same, but on GBIF they seem to have a different `taxonKey`. This case is not catched by the application.

## Improvements of the application
This is a first version of the application, and many improvements and extentions can be imagined. Some possible ideas are:
* Implement a logic to take the liste of 'Type' specimen and discover the kind of type the specimen could/should be
* The interface with the Biodiversity Heritage Library (BHL) is implemented in the scripts, but is not yet integrated in the application
* Better integration of the information that can be extracted from Wikidata

## Structure of the repository

The repository contains two main folders. The 'notebooks' folder is a selection of Jupyter notebooks that were used to explore the possibilities with the different APIs and how this information can be extracted.

The real code is contained in the 'linkedTaxonomy' folder. This folder contains a python Flask application. The application takes Genus and epithet as input to run the checks on nomenclature and build the information known on this taxon. A timeline is built to show the history of this taxon.

```bash
|-- requirements.txt
|-- LICENSE
|-- README.md
|-- notebooks
    |-- Name_information_types.ipynb
    |-- Types_GBIFonly.ipynb
    |-- Wikidata_taxon.ipynb
|-- linkedTaxonomy
    |-- app.py
    |-- static
        |-- images
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

## Installation and usage instructions

### Jupyter/Google Colab notebooks
Some of the development of this application was performed in Jupyter notebooks. While all of the fuctionalities in these notebooks are transferred to the Python application, you might find it usefull to have a look at these notebooks and play around with them. Be aware that not


### Installation
Make sure that Python >= 3.6 is installed on your machine. In order to install the nessesary dependencies, please run in the main folder:

```bash
pip3 install -r requirements.txt
```

In order to start the application, go to the folder `\linkedTaxonomy` and run:

```bash 
python3 app.py
```
This will start a development server running on `http:\\localhost:5000`. In order to deploy this application on a server, you should setup a WSGI interface and a server (e.g. Apache)

### Usage of the application
The home page of the application gives you a list of possible taxa extracted from Wikidata. This list is created by the following rule: all taxa with an IPNI ID and a Plazi ID. An extra filter is applied which excludes results with a ZooBank ID, since these treatments are often not accesible. The namese are clickable and start the actual application. However, the application works for other taxa as well.

To start the actual appliction, the structure of the URL to pass is:
```
http://localhost:5000/<Genus>/<epithet>
```
Carefull: the syntax is case sensitive. The genus should always start with a capital/



## References
To be added
