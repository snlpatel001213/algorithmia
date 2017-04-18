import requests
import json
from bs4 import BeautifulSoup
import urllib2
import re
import codecs
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def applyFilters(text):
        filteredtext = re.sub(r"(\|\S\|)", "|", text)
        filteredtext = re.sub(r"^\|", "", filteredtext)
        filteredtext = re.sub(r"\|$", "", filteredtext)
        filteredtext = re.sub(r"\[\d+\]", "", filteredtext)
        # print filteredtext
        return filteredtext


def searchDuckDuckGo(searchFor):
        InfoDict = {}
        InfoDict['searchedTitle'] = searchFor

        InfoDict['url']=""
        response = json.loads(requests.get("https://duckduckgo.com/?q="+searchFor+"&ia=web&format=json", verify = False).text)
        if response['Infobox']: # if found infobox with first search
            for eachField in response['Infobox']['content']:
                # print eachField['label'], eachField['value']
                InfoDict[str(eachField['label'])+"_duckduckgo"] = str(eachField['value'])

            # print response['AbstractURL']
            InfoDict['url'] = response['AbstractURL']
            # print response['AbstractText']
            InfoDict['Abstract'] = response['AbstractText']
            # print response['Image']
            InfoDict['poster'] = response['Image']
        elif response['Infobox'] == "": # if found infobox with modified search
            searchFor = searchFor + " movie"
            response = json.loads(
                requests.get("https://duckduckgo.com/?q=" + searchFor + "&ia=web&format=json", verify=False).text)
            if response['Infobox']:
                # print len(response['Infobox']['content'])
                for eachField in response['Infobox']['content']:
                    InfoDict[str(eachField['label'])] = str(eachField['value'])
                # print response['AbstractURL']
                InfoDict['url'] = response['AbstractURL']
                # print response['AbstractText']
                InfoDict['Abstract'] = response['AbstractText']
                # print response['Image']
                InfoDict['poster'] = response['Image']
        return InfoDict

def searchWikipedia(searchedDuckDuckGo):
    """
    searchedDuckDuckGo is a dictionary having information about movie, we will use this further for more in formation
    :param searchedDuckDuckGo:
    :return:
    """

    if searchedDuckDuckGo['url'] != "":
        wikipediaURl = searchedDuckDuckGo['url']
        print wikipediaURl
        response = urllib2.urlopen(wikipediaURl)
        html = response.read()
        soup = BeautifulSoup(html)

        infotable = soup.find("table", {"class": "infobox vevent"})
        allRows =  infotable.find_all("tr")
        searchedDuckDuckGo['title_wikipedia'] = str(allRows[0].text).replace("\n", "").strip()
        for row in allRows[2:]:
            for td in row.find_all("td"):
                searchedDuckDuckGo[applyFilters(str(row.findAll('th')[0].text).strip().replace("\n", ""))+"_wikipedia"] = applyFilters(td.text.replace("\n", "|"))
                # print applyFilters(td.text.replace("\n", "|")), " % ", applyFilters(
                #     str(row.findAll('th')[0].text).strip().replace("\n", ""))
        return searchedDuckDuckGo

#Search duckduckgo
searchedDuckDuckGo =  searchDuckDuckGo("the goonies")
# print searchedDuckDuckGo
#Search Wikipedi
print searchWikipedia(searchedDuckDuckGo)