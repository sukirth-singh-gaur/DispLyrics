from bs4 import BeautifulSoup
import requests
import json
            
html_text = requests.get('   https://search.azlyrics.com/search.php?q=zaalima&x=6a377bfc3a3ba6a7b9e087ad7cc5cfca8b1623295d4b8553a8669b8de83bc37a').text
soup = BeautifulSoup(html_text,'lxml');

topPanel = soup.find('div',class_ = 'panel-heading')
panelText = topPanel.small.text.replace(' ','');
NumberOfResults = panelText[3];
print(NumberOfResults);

songResults = []

songs = soup.findAll('td',class_ ='text-left visitedlyr')
for i in range(int(NumberOfResults)):
    songResult = {}
    songResult['song_name'] = songs[i].text.strip();
    print(songResult['song_name'])
    songResults.append(songResult)

with open("./popup/resultsFound.json","w") as file:
    json.dump(songResults,file)


