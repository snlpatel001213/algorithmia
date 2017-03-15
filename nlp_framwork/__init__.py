from spacy.en import English

parser = English()
from itertools import tee, islice
import re
from bs4 import BeautifulSoup

import requests
import json
import re
import urllib
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
from collections import Counter
import enchant
import requests
import json
import urllib
from bs4 import BeautifulSoup

d = enchant.Dict("en_US")
from nltk.corpus import stopwords

ratingDict = {}
stop = set(stopwords.words('english'))
multiSentence = u'''About Rustom Movie
Rustom is a Bollywood movie. Rustom movie releasing date is 12 Aug 2016. Movie Rustom based on romance, crime and thriller. The lead actor of Rustom movie is Akshay Kumar. Who is playing role of Rustom Pavri. The lead actress name of Rustom movie is Ileana D'Cruz and Esha Gupta. Rustom is also based on life of Naval Officer K.M. Nanavati. Rustom movie budget should be approx 65 crores.

Click To See Upcoming Movies List

Release Date-12 Aug 2016
Movie Budget-65 Crores
Genre-Romance, Thriller, Crime
Movie Director-Tinu Suresh Desai
Music Director-Ankit Tiwari, Jeet Ganguly, Raghav Sachar, Arko Pravo Mukherjee
Producer-Neeraj Pandey, Aruna Bhatia, Nittin Keni, Akash Chawla, Virender Arora, Ishwar Kapoor, Shiital Bhatia
Banner-A Friday Filmworks, KriArj Entertainment Pvt. Ltd, Essel Vision Productions Ltd, Cape of Good Films.
Cinematography-Santosh Thundiyil
Written By-Vipul K. Rawal
Choreographer-N/A
Running Time- N/A
Status-Released'''
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

parsedData = parser(multiSentence)
sents = []
for span in parsedData.sents:
    print  ''.join(parsedData[i].string for i in range(span.start, span.end)).strip()
print "#"*100
ents = list(parsedData.ents)
for entity in ents:
    # print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
    # if(entity.label_ == 'PERSON'):
    print ' '.join(t.orth_ for t in entity)
print "#"*100
for span in parsedData.sents:
    sent = [parsedData[i] for i in range(span.start, span.end)]
    for token in sent:
        if( token.pos_=='PROPN'):
            print token.orth_


