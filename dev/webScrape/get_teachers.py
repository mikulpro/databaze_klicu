"""
Stáhne data o učitelích FŽP ze stagu a uloží do "ucitele_fzp.json"
"""

import requests, json
from bs4 import BeautifulSoup


fakulta = "FZP"

data = f"type=katedra&varName=G230413suggestor&katedraInput=%25&krouzekSearchFakulta={fakulta}&searchCisloPracoviste=%25&prohlizeniPracovisteJenPlatna=A&porLo=cs"

r = requests.get('https://portal.ujep.cz/StagPortletsJSR168/StagSuggest', data)

soup = BeautifulSoup(r.text)
workplaces = [i.get_text() for i in soup.find_all('a')][:-1]
teachers = {}

for workplace in workplaces:
    short = workplace.split(",")[0]
    data = f"type=ucitel&varName=G230413ucitelSuggest&katedraInput={short}&ucitelInput=%25&ucitelJmeno=%25&porLo=cs"

    r = requests.get('https://portal.ujep.cz/StagPortletsJSR168/StagSuggest', data)
    soup = BeautifulSoup(r.text)
    t = [i.get_text() for i in soup.find_all('a')][:-1]

    teachers[workplace] = t

print(teachers)
with open("ucitele_fzp.json", "w") as out:
    out.write(json.dumps(teachers))