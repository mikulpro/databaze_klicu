from bs4 import BeautifulSoup
import requests
import json

# aplikace session pro ukladani cookies
session = requests.Session()

# base url, ktery je vzdy na zacatku api stejny
base_url = 'https://stag-demo.zcu.cz/ws/services/rest2'
p = {
    'domena': 'ANO_NE',
    'outputFormat': 'JSON'
}
res = session.get(f'{base_url}/ciselniky/getCiselnikNewItems', params=p)
res_post = session.post(f'{base_url}/cesta', data={})

json_text = json.loads(res.text)

print(json_text['item'][0]['valueEn'])

base_url = 'https://portal.ujep.cz'
p = {
    'type':'katedra',
    'varName':'G231555suggestor',
    'katedraInput':'%',
    'predmetInput':'%',
    'mistnostSearchBudova':'%',
    'mistnostCislo':'%',
    'raVyucujici':'%',
    'raDen':'%',
    'raSemestr':'%',
    'raTyp':'%',
    'raRok':'2023',
    'raHodinaOd':'0',
    'raHodinaDo':'99',
    'raCasOd':'00%3A00',
    'raCasDo':'23%3A59',
    'raTydenOdOd':'1',
    'raTydenOdDo':'53',
    'raTydenDoOd':'1',
    'raTydenDoDo':'53',
    'raTypTydne':'%',
    'raPlatnost':'A',
    'raPlanOd':'0',
    'raPlanDo':'999',
    'raObsazeniOd':'0',
    'raObsazeniDo':'999',
    'raObsazeniProcOd':'0',
    'raObsazeniProcDo':'100',
    'raRozvrhar':'%',
    'raKontakt':'%',
    'raGrupa':'%',
    'raMistnostProVyuku':'%',
    'porLo':'cs',
}
res = session.post(f'{base_url}/StagPortletsJSR168/StagSuggest', data=p)
soup = BeautifulSoup(res.text, 'html.parser')
for child in soup.find('div').children:
    print(f'hello: {child}')