import json


data = json.load(open('ucitele.json'))
data2 = json.load(open('ucitele_fzp.json'))

data.update(data2)


all = []
for i in data.values():
    for j in i:
        a = j.split(",")
        if len(a) >= 3:
            all.append(a[2])
        if len(a) >= 4:
            all.append(a[3])

a2 = []
for i in all:
    a2.append(i.split("-")[0])

titles = set()
for i in a2:
    for j in i.split(" "):
        if len(j) > 0:
            titles.add(j)

print(titles)
