from bs4 import BeautifulSoup
import requests
def GetTraits(url):
    HTML = requests.get(url)
    soup = BeautifulSoup(HTML.content, 'lxml')
    divs = soup.findAll('div')

    traits = {"back":"",
            "body":"",
            "eyes":"",
            "mouth":"",
            "flavor":"",
            "clothes":"",
            "headwear":"",
            "lefthand":"",
            "righthand":"",
            "background":""}

    for index,div in enumerate(divs):
        if div.text == 'Attributes / back':
            traits["back"] = divs[index + 2].text
        elif div.text == 'Attributes / body':
            traits["body"] = divs[index + 2].text
        elif div.text == 'Attributes / eyes':
            traits["eyes"] = divs[index + 2].text
        elif div.text == 'Attributes / mouth':
            traits["mouth"] = divs[index + 2].text
        elif div.text == 'Attributes / flavor':
            traits["flavor"] = divs[index + 2].text
        elif div.text == 'Attributes / clothes':
            traits["clothes"] = divs[index + 2].text
        elif div.text == 'Attributes / headwear':
            traits["headwear"] = divs[index + 2].text
        elif div.text == 'Attributes / left hand':
            traits["lefthand"] = divs[index + 2].text
        elif div.text == 'Attributes / background':
            traits["background"] = divs[index + 2].text
        elif div.text == 'Attributes / right hand':
            traits["righthand"] = divs[index + 2].text
    GoombleID = divs[108].text[8:]
    return traits,GoombleID



    
    
    
    
    
    
    
    
     
    
