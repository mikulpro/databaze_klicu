import json

with open('webScrape/ucitele.json') as file:
    ucitele = json.loads(file.readline())

with open('webScrape/ucitele_fzp.json') as file:
    ucitele_fzp = json.loads(file.readline())


ucitele.update(ucitele_fzp)


ucitele_dicts = {}
r_id = 1
for workplace_str in ucitele.keys():
    for j in ucitele[workplace_str]:
        data_str, workplaces_str = j.split(' - ')
        if ucitele_dicts.get(data_str):
            ucitele_dicts[data_str]['workplaces'].append(workplace_str.split(',')[0])
        else:
            data = data_str.split(', ')
            firstname = data[1]
            surname = data[0]
            titles1 = data[2].split(' ') if len(data) > 2 else []
            if 'ak.' in titles1:
                index = titles1.index('ak.')
                titles1[index] = titles1[index] + ' ' +  titles1[index+1]
                titles1.pop(index+1)
            titles2 = data[3].split(' ') if len(data) > 3 else []
            ucitele_dicts[data_str] = {
                'id': r_id,
                'firstname': firstname,
                'surname': surname,
                'titles1': titles1,
                'titles2': titles2,
                'workplaces': [workplace_str.split(',')[0]]
            }
            r_id += 1
            
ucitele_out = list(ucitele_dicts.values())

# zadny ucitel podle stagu neni zamestnancem vice pracovist
print(ucitele_out)

with open('webScrape/ucitele2.json', 'w') as file:
    file.write(json.dumps(ucitele_out))

with open(f"../data/data_Borrowers.csv", "w") as outfile:
    for ucitel in ucitele_out:
        outfile.write(str(ucitel['id'])+';')
        outfile.write(str(ucitel['firstname']) + ';')
        outfile.write(str(ucitel['surname']) + ';')

        outfile.write("\n")