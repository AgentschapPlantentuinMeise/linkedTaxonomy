
def include_images(iList):
    
    test = """
    """

    for image in iList:
        test = """{0} 
        
        <div class="w3-col m3">
            <img src="{1}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Picture from the treatments">
            </div>""".format(test,image)


    message = """<div class="w3-content w3-container w3-padding-64" id="portfolio">
        <h3 class="w3-center">IMAGES</h3>
            <p class="w3-center"><em>Here are some images.<br> Click on the images to make them bigger</em></p><br>

          <!-- Responsive Grid. Four columns on tablets, laptops and desktops. Will stack on mobile devices/small screens (100% width) -->
          <div class="w3-row-padding w3-center">
            {0}

        <button class="w3-button w3-padding-large w3-light-grey" style="margin-top:64px">LOAD MORE</button>
      </div>
    </div>
    """.format(test)

    return message

if __name__ == '__main__':
    
    import sys
    list1 = ['test1','test2','test3']
    output = include_images(list1)
    print(output)
