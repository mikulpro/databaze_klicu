import json, csv

with open('../../webScrape/ucitele2.json', 'r') as file:
    borrowers = json.loads(file.readline())

titles = {}
titles_is_before = {}
with open('../data/data_Titles.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for i in reader:
        titles[i[1]] = i[0]
        titles_is_before[i[1]] = i[2]

print(titles)
print(titles_is_before)

borrowers_titles = []

for borrower in borrowers:
    order = 1
    if borrower['titles1']:
        for title in borrower['titles1']:
            if title == 'Dr.':
                if borrower['titles2']:
                    title_id = 18
                elif len(borrower['titles1']) > 1:
                    index = 1 if borrower['titles1'].index('Dr.') == 0 else 0
                    if titles_is_before[borrower['titles1'][index]]:
                        title_id = 18
                    else:
                        title_id = 19
                else:
                    title_id = 18
            else:
                title_id = int(titles[title])
            is_before = True if titles_is_before[title] else False
            borrowers_titles.append((
                borrower['id'],
                title_id,
                order
            ))
            order += 1
    if borrower['titles2']:
        is_before = False
        for title in borrower['titles2']:
            if title != "et":
                borrowers_titles.append((
                    borrower['id'],
                    int(titles[title]),
                    order
                ))
                order += 1

print(borrowers_titles)

with open('../data/data_BorrowersTitles.csv', 'w') as outfile:
    for i in borrowers_titles:
        outfile.write(f"{i[0]};{i[1]};{i[2]}\n")
