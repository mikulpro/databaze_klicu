"""
Stáhne data o učebnách ze stagu a uloží do "ucebny.json"
"""

from bs4 import BeautifulSoup
import json
import requests


data = {
    "type": "mistnost",
    "varName": "G230413suggestor",
    "mistnostSearchBudova": "CP",
    "mistnostCislo": "CP-4%",
    "mistnostSearchPracoviste": "%",
    "mistnostKapacitaOd": "0",
    "mistnostKapacitaDo": "999",
    "mistnostJenPlatne": "A",
    "search": "true",
    "porLo": "cs",
}


rooms = {}

for floor_num in range(-1, 9):
    data["mistnostCislo"] = f"CP-{floor_num}%"
    data_str = "&".join(["=".join(i) for i in data.items()])

    r = requests.get('https://portal.ujep.cz/StagPortletsJSR168/StagSuggest', data_str)
    html = r.text

    soup = BeautifulSoup(html, features="html.parser")

    rooms_text = [i.get_text() for i in soup.find_all('a')][:-1]
    floor = []

    for text in rooms_text:
        a = text.split(" ")
        print(a[0])
        room = {
        'name': a[0],
        'type': a[1][:-1],
        'num': a[2],
        'faculty': a[3][1:-1]
        }
        floor.append(room)

    rooms[floor_num] = floor


with open("ucebny.json", "w") as out:
    out.write(json.dumps(rooms))
