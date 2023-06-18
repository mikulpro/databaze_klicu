# cesta stag: /ws/services/rest2
# pouzivat knihovnu REQUESTS, json

import requests
import json

# opakujici se casti
base_url = 'https://stag-demo.zcu.cz/ws/services/rest2'
p={'domena':'ANO_NE', 'outputFormat':'JSON'}

# OTAZNIK V ODKAZU ODDELUJE PARAMETRY
response = requests.get(f'{base_url}/ciselniky/getCiselnikNewItems', params=p)
json_text = json.loads(response.text)
print(json.dumps(json_text, indent=2, sort_keys=True))

# ziskavani dat z json
print(json_text['item'][0]['valueEn'])

# prihlasovani se pomoci session
session_object = requests.Session()
response = session_object.get(f'{base_url}/ciselniky/getCiselnikNewItems', params=p)
json_text = json.loads(response.text)
print(json_text['item'][0]['valueEn'])

# res_post session / request je pak k odesilani dat na server
# bude v od_Honzy.py