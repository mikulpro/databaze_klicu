import json

with open('../../webScrape/ucitele.json') as file:
    data = file.readline()

ucitele_prf = json.loads(data)

workplaces = []

for workplace_str in ucitele_prf.keys():
    workplace_split = workplace_str.split(', ')
    # abbreviation, name, faculty
    workplaces.append((
        workplace_split[0],
        workplace_split[1],
        1
    ))


with open('../../webScrape/ucitele_fzp.json') as file:
    data = file.readline()

ucitele_fzp = json.loads(data)

for workplace_str in ucitele_fzp.keys():
    workplace_split = workplace_str.split(', ')
    # abbreviation, name, faculty
    workplaces.append((
        workplace_split[0],
        workplace_split[1],
        2
    ))

print(workplaces)

r_id = 1
with open(f"../data/data_Workplaces.csv", "w") as outfile:
    for row in workplaces:
        outfile.write(str(r_id)+';')
        for i in range(len(row)):
            outfile.write(str(row[i]))
            if i < (len(row)-1):
                outfile.write(";")
        outfile.write("\n")
        r_id += 1
