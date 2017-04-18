#-*-coding:utf8-*-
import requests
import json
from bs4 import BeautifulSoup
import urllib2
import codecs
import re

html = """<table class="infobox vevent" style="width:22em;font-size:90%;">
<tr>
<th class="summary" colspan="2" style="text-align:center;font-size:125%;font-weight:bold;font-size:110%;font-style:italic;">Escape Plan</th>
</tr>
<tr>
<td colspan="2" style="text-align:center"><a class="image" href="/wiki/File:Escapeplanfilmposter.jpg"><img alt="Escapeplanfilmposter.jpg" class="thumbborder" data-file-height="428" data-file-width="300" height="314" src="//upload.wikimedia.org/wikipedia/en/thumb/5/5d/Escapeplanfilmposter.jpg/220px-Escapeplanfilmposter.jpg" srcset="//upload.wikimedia.org/wikipedia/en/5/5d/Escapeplanfilmposter.jpg 1.5x" width="220"/></a>
<div style="font-size:95%;padding:0.35em 0.35em 0.25em;line-height:1.25em;">Theatrical release poster</div>
</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Directed by</th>
<td style="line-height:1.3em;"><a href="/wiki/Mikael_H%C3%A5fstr%C3%B6m" title="Mikael Håfström">Mikael Håfström</a></td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Produced by</th>
<td style="line-height:1.3em;">
<div class="plainlist">
<ul>
<li><a href="/wiki/Mark_Canton" title="Mark Canton">Mark Canton</a></li>
<li>Randall Emmett</li>
<li>Remington Chase</li>
<li><a href="/wiki/Robbie_Brenner" title="Robbie Brenner">Robbie Brenner</a></li>
<li>Kevin King-Templeton</li>
</ul>
</div>
</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Screenplay by</th>
<td style="line-height:1.3em;">Miles Chapman<br/>
<a href="/wiki/Jason_Keller_(playwright)" title="Jason Keller (playwright)">Arnell Jesko</a></td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Story by</th>
<td style="line-height:1.3em;">Miles Chapman</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Starring</th>
<td style="line-height:1.3em;">
<div class="plainlist">
<ul>
<li><a href="/wiki/Sylvester_Stallone" title="Sylvester Stallone">Sylvester Stallone</a></li>
<li><a href="/wiki/Arnold_Schwarzenegger" title="Arnold Schwarzenegger">Arnold Schwarzenegger</a></li>
<li><a href="/wiki/Jim_Caviezel" title="Jim Caviezel">Jim Caviezel</a></li>
<li><a href="/wiki/50_Cent" title="50 Cent">Curtis "50 Cent" Jackson</a></li>
<li><a href="/wiki/Sam_Neill" title="Sam Neill">Sam Neill</a></li>
<li><a href="/wiki/Vinnie_Jones" title="Vinnie Jones">Vinnie Jones</a></li>
<li><a href="/wiki/Vincent_D%27Onofrio" title="Vincent D'Onofrio">Vincent D'Onofrio</a></li>
<li><a href="/wiki/Amy_Ryan" title="Amy Ryan">Amy Ryan</a></li>
</ul>
</div>
</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Music by</th>
<td style="line-height:1.3em;"><a href="/wiki/Alex_Heffes" title="Alex Heffes">Alex Heffes</a></td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Cinematography</th>
<td style="line-height:1.3em;">Brendan Galvin</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Edited by</th>
<td style="line-height:1.3em;">Elliot Greenberg</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">
<div style="padding:0.1em 0;line-height:1.2em;">Production<br/>
company</div>
</th>
<td style="line-height:1.3em;">
<div style="vertical-align:middle;">Atmosphere Entertainment<br/>
<a href="/wiki/Emmett/Furla/Oasis_Films" title="Emmett/Furla/Oasis Films">Emmett/Furla Films</a></div>
</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Distributed by</th>
<td style="line-height:1.3em;"><a href="/wiki/Summit_Entertainment" title="Summit Entertainment">Summit Entertainment</a></td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">
<div style="padding:0.1em 0;line-height:1.2em;white-space:normal;">Release date</div>
</th>
<td style="line-height:1.3em;">
<div class="plainlist">
<ul>
<li>October 9, 2013<span style="display:none"> (<span class="bday dtstart published updated">2013-10-09</span>)</span> <span class="nowrap"><small>(Philippines<sup class="reference" id="cite_ref-PhilStar_1-0"><a href="#cite_note-PhilStar-1">[1]</a></sup>)</small></span></li>
<li>October 18, 2013<span style="display:none"> (<span class="bday dtstart published updated">2013-10-18</span>)</span> <span class="nowrap"><small>(United States<sup class="reference" id="cite_ref-2"><a href="#cite_note-2">[2]</a></sup>)</small></span></li>
<li class="mw-empty-elt"></li>
<li class="mw-empty-elt"></li>
<li class="mw-empty-elt"></li>
</ul>
</div>
</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">
<div style="padding:0.1em 0;line-height:1.2em;white-space:normal;">Running time</div>
</th>
<td style="line-height:1.3em;">115 minutes<sup class="reference" id="cite_ref-3"><a href="#cite_note-3">[3]</a></sup></td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Country</th>
<td style="line-height:1.3em;">United States</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Language</th>
<td style="line-height:1.3em;">English</td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Budget</th>
<td style="line-height:1.3em;">$50 million<sup class="reference" id="cite_ref-Deadline_4-0"><a href="#cite_note-Deadline-4">[4]</a></sup></td>
</tr>
<tr>
<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Box office</th>
<td style="line-height:1.3em;">$137.3 million<sup class="reference" id="cite_ref-Mojo_5-0"><a href="#cite_note-Mojo-5">[5]</a></sup></td>
</tr>
</table>"""

def applyFilters(text):
    filteredtext = re.sub(r"(\|\S\|)", "|", text)
    filteredtext = re.sub(r"^\|", "", filteredtext)
    filteredtext = re.sub(r"\|$", "", filteredtext)
    filteredtext = re.sub(r"\[\d+\]", "", filteredtext)
    # print filteredtext
    return filteredtext

soup = BeautifulSoup(html)

for row in soup.find_all("tr")[2:]:
    for td in row.find_all("td"):
        print applyFilters(td.text.replace("\n","|"))," % ",applyFilters(str(row.findAll('th')[0].text).strip().replace("\n",""))

