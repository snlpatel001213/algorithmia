# -*-coding:utf-8-*-
from spacy.en import English

parser = English()
from itertools import tee, islice
from collections import Counter
import enchant
from bs4 import BeautifulSoup

d = enchant.Dict("en_US")
from nltk.corpus import stopwords
import requests
import re
import urllib
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

ratingDict = {}
stop = set(stopwords.words('english'))


def scrorer(Name):
    try:
        ratingDict[Name] += 10
    except KeyError:
        ratingDict[Name] = 10


def duckSearch(searchList, numberOFSeraches):
    """
    :param searchList:
    :param numberOFSeraches:
    :return: list of urls
    """
    query = '+'.join(searchList)
    query = query.replace(" ", "+")
    print 'http://duckduckgo.com/?q=' + query
    site = urllib.urlopen('http://duckduckgo.com/html/?q=' + query, context=ctx)
    data = site.read()
    parsed = BeautifulSoup(data)

    returnUrlsList = []
    for i in range(0, numberOFSeraches):
        returnUrlsList.append(parsed.findAll('div', {'class': 'result__extras__url'})[i].a['href'])
    return returnUrlsList


def pageContentGrabber(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def nameEntitySpacy(multiSentence):
    parsedData = parser(multiSentence)
    sents = []
    # for span in parsedData.sents:
    #     # go from the start to the end of each span, returning each token in the sentence
    #     # combine each token using join()
    #     sent = ''.join(parsedData[i].string for i in range(span.start, span.end)).strip()
    #     sents.append(sent)

    # for sentence in sents:
    #     print(sentence)
    #
    # for span in parsedData.sents:
    #     sent = [parsedData[i] for i in range(span.start, span.end)]
    #     break

    # parsedEx = parsedData
    # # shown as: original token, dependency tag, head word, left dependents, right dependents
    # for token in parsedEx:
    #     print(
    #     token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])

    # for token in sent:
    #     print(token.orth_, token.pos_)
    # for token in parsedData:
    #     print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")

    print("-------------- entities only ---------------")
    # if you just want the entities and nothing else, you can do access the parsed examples "ents" property like this:
    ofInterest = []

    for span in parsedData.sents:
        sent = [parsedData[i] for i in range(span.start, span.end)]
        for token in sent:
            if (token.pos_ == 'PROPN'):
                ofInterest.append(token.orth_)

    # ents = list(parsedData.ents)
    # for entity in ents:
    #     # print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
    #     # if(entity.label_ == 'PERSON'):
    #     ofInterest.append(' '.join(t.orth_ for t in entity))
    # print ofInterest
    return ofInterest


def ngrams(lst, n):
    """
    nonEnglishLine = ""
    nonEnglisharray = []
    # print multiSentence.split(" ")
    for line in multiSentence.split(" "):
        if (d.check(line.strip()) == True):
            pass
        else:
            nonEnglisharray.append(line)

    nonEnglishLine = " ".join(nonEnglisharray)
    nonEnglisharray = [i for i in nonEnglishLine.lower().split() if i not in stop]
    nonEnglishLine = " ".join(nonEnglisharray)
    # print nonEnglishLine
    words = re.findall("\w+", nonEnglishLine)
    print Counter(ngrams(words, 1))

    :param lst:
    :param n:
    :return:
    """
    tlst = lst
    while True:
        a, b = tee(tlst)
        l = tuple(islice(a, n))
        if len(l) == n:
            yield l
            next(b)
            tlst = b
        else:
            break


def chunkingAndCollocationFinder(multiSentence):
    """
    :param multiSentence: is text from html
    :return: updates dictionary Nothing goes out
    """
    # multiSentence=unicode(multiSentence, "utf-8")
    nonEnglishLine = " ".join(nameEntitySpacy(multiSentence))
    print "nonEnglishLine"
    print nonEnglishLine
    words = re.findall("\w+", nonEnglishLine)
    print Counter(ngrams(words, 2))

    parsedData = parser(multiSentence)
    sents = []
    for span in parsedData.sents:
        sent = ''.join(parsedData[i].string for i in range(span.start, span.end)).strip()
        sents.append(sent)
    directorSynonymes = ['ingredient', 'ingredients', 'api']
    for i in sorted(Counter(ngrams(words, 2))):
        # print " ".join(i) # got all the relevant names
        for sent in sents:
            for synonymes in directorSynonymes:
                if (synonymes in sent.lower() and " ".join(i).lower() in sent.lower()):
                    scrorer(" ".join(i))  # scoring
                    print "ingredient", " ".join(i)

    for i in sorted(Counter(ngrams(words, 3))):
        # print " ".join(i) # got all the relevant names
        for sent in sents:
            for synonymes in directorSynonymes:
                if (synonymes in sent.lower() and " ".join(i).lower() in sent.lower()):
                    scrorer(" ".join(i))  # scoring
                    print "ingredient", " ".join(i)
                    # print ratingDict


###############Start##############################
# Sarching for 'director' and 'movie'
InitialSearch = ['ingredient of', 'aspirin']
InitialSearchResultURLS = duckSearch(InitialSearch, 3)
print InitialSearchResultURLS
for url in InitialSearchResultURLS:
    pageContent = pageContentGrabber(url)
    print pageContent
    chunkingAndCollocationFinder(pageContent)
###############AdvanceSearch######################
# SecondSearch
for key in ratingDict:
    InitialSearch = ['ingredient of', 'aspirin', key]  # "key is the name of the person who is supposed to be director"
    InitialSearchResultURLS = duckSearch(InitialSearch, 3)
    for url in InitialSearchResultURLS:
        pageContent = pageContentGrabber(url)
        chunkingAndCollocationFinder(pageContent)
print ratingDict
