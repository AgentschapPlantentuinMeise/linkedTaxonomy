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

app = Flask(__name__)

@app.route('/')
def home(table=None):
    df = wikidata.list_wd()
    print(df.to_html(classes='data', header='true', max_rows=10))
    return render_template('home.html', tables=[df.to_html(classes='data', header='true')])

@app.route('/<genus>/<species>')
def taxon(genus=None, species=None):
    treatments = plazi.get_treatments(genus,species)
    images = []
    publications = []
    type_information = []

    for treatment in treatments:
        p,f,t = plazi.get_treatment_information(treatment)
        images.extend(f)
        publications.extend(p)
        type_information.extend(t)

    image_list = lt_html.include_images(images)
    for item in type_information:
        date_p, collections_p = protologue.find_collections(item)
        print(date_p)
        print(collections_p)
    
    
    return render_template('taxon.html', genus=genus, species=species, image_list=image_list)


if __name__ == '__main__':

     app.run(port=5000,debug=True)
