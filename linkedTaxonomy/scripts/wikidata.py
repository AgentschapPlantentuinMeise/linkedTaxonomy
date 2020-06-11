import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

def list_wd():

    wd_endpoint = 'https://query.wikidata.org/sparql'
    wd_query = ''' select ?item ?itemLabel ?ipni ?plaziID where {
                        ?item wdt:P31 wd:Q16521;
                              wdt:P105 wd:Q7432;
                              wdt:P961 ?ipni;
                              wdt:P1992 ?plaziID.
                    FILTER NOT EXISTS {?item wdt:P1746 ?zoo.}.
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }
                LIMIT 2000 '''

    r = requests.get(wd_endpoint, params= {'format' : 'json', 'query' : wd_query})
    if r.status_code == 200:
        result = json.loads(r.text)
        cols = result['head']['vars']
        out = []
        for row in result['results']['bindings']:
            item = []
            for c in cols:
                item.append(row.get(c, {}).get('value'))
            out.append(item)
        return pd.DataFrame(out,columns=cols)
    else:
        return None


if __name__ == "__main__":
    results = list_wd()
    print(results)
