import json
import requests
import pandas as pd

def get_collection(code):

    url = 'http://sweetgum.nybg.org/science/api/v1/institutions/' + code
    collection = requests.get(url)


    if collection.status_code == 200:

        collections = json.loads(collection.text)
        collections = {'code' : collections['code'], 'name' : collections['organization'], 'website' : collections['contact']['webUrl']}
        df = pd.DataFrame(collections, index=[0])
        return df

    else:

        return None

def get_collectionsList(collectionsIDs):

    columns = ['code', 'name', 'website']
    df = pd.DataFrame(columns=columns)

    for code in collectionsIDs:
        if code != 'J': # this is a bug to be fixed Issue#2
            pdf = get_collection(code)
            if pdf is not None:
                df = df.append(pdf, ignore_index=True)

    return df

if __name__ == "__main__":
    import sys
    output = globals()[sys.argv[1]](sys.argv[2])
    print(output)
