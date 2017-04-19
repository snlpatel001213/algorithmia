import wikipedia
from bs4 import BeautifulSoup
import urllib2
import re
import traceback


def applyFilters(text):
    filteredtext = re.sub(r"(\|\S\|)", "|", text)
    filteredtext = re.sub(r"^\|", "", filteredtext)
    filteredtext = re.sub(r"\|$", "", filteredtext)
    filteredtext = re.sub(r"\[\d+\]", "", filteredtext)
    # print filteredtext
    return filteredtext
def getInfoFromWikipediaUrl(wikipediaURL):
    searchedDuckDuckGo = {}
    response = urllib2.urlopen(wikipediaURL)
    searchedDuckDuckGo['wikipediaUrl'] = wikipediaURL
    html = response.read()
    soup = BeautifulSoup(html)

    infotable = soup.find("table", {"class": "infobox vevent"})
    allRows = infotable.find_all("tr")
    searchedDuckDuckGo['title_wikipedia'] = str(allRows[0].text).replace("\n", "").strip()
    for row in allRows[2:]:
        for td in row.find_all("td"):
            searchedDuckDuckGo[applyFilters(
                str(row.findAll('th')[0].text).strip().replace("\n", "")) + "_wikipedia"] = applyFilters(
                td.text.replace("\n", "|"))
    print  searchedDuckDuckGo


def searchInWikiPedia(SearchTerm):
    try:
        url = wikipedia.page(SearchTerm).url
        print url
        getInfoFromWikipediaUrl(url)
    except Exception as e :
        print str(e)
        alternativeUrl =  re.sub(r"^.*may refer to:(.*)",r"\1",str(e).replace("\n","|"))
        alternativeUrl =  alternativeUrl.split("|")
        print alternativeUrl
        for eachWikiName in alternativeUrl:
            try:
                if eachWikiName.isspace() == False:
                    wikipediaURL  = wikipedia.page(eachWikiName).url
                    print eachWikiName,wikipediaURL
                    getInfoFromWikipediaUrl(wikipediaURL)
            except:
                print traceback.print_exc()

