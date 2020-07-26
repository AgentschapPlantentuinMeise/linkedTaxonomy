import pandas as pd
import json
from pandas.io.json import json_normalize

def make_gbif_specimen_link(gbifID):

    url = '<a target="_blank" href="https://www.gbif.org/occurrence/{0}">{0}</a>'.format(gbifID)

    return url


def make_specimen_table(df):


    columns = ['gbifID', 'scientificName', 'recordedBy', 'eventDate', 'collectionCode', 'institutionCode', 'countryCode', 'recordNumber']

    
    sdf = df.reindex(columns=columns)
    sdf['gbifID'] = sdf['gbifID'].apply(lambda x: make_gbif_specimen_link(x))
    sdf.replace('', '&nbsp;', inplace=True)

    message = sdf.to_html(classes='data', header=True, index=False, escape=False)

    return message



def include_images(iList):
    
    test = """
    """

    for image in iList:
        test = """{0} 
        
        <div class="w3-col m3">
            <img src="{1}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Picture from the treatments">
            </div>""".format(test,image)


    message = """<div class="w3-content w3-container w3-padding-64" id="images">
        <h3 class="w3-center">IMAGES</h3>
            <p class="w3-center"><em>Here are some images.<br> Click on the images to make them bigger</em></p><br>

          <!-- Responsive Grid. Four columns on tablets, laptops and desktops. Will stack on mobile devices/small screens (100% width) -->
          <div class="w3-row-padding w3-center">
            {0}

      </div>
    </div>
    """.format(test)

    return message

if __name__ == '__main__':
    
    import sys
    list1 = ['test1','test2','test3']
    output = include_images(list1)
    print(output)
