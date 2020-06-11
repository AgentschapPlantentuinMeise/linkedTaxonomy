import sys
sys.path.append('./scripts/')

from flask import render_template

from flask import Flask, url_for
from markupsafe import escape
import wikidata

app = Flask(__name__)

@app.route('/')
def home(table=None):
    df = wikidata.list_wd()
    print(df.to_html(classes='data', header='true', max_rows=10))
    return render_template('home.html', tables=[df.to_html(classes='data', header='true')])

@app.route('/<genus>/<species>')
def taxon(genus=None, species=None):
    return render_template('taxon.html', genus=genus, species=species)


if __name__ == '__main__':

     app.run(port=5000,debug=True)
