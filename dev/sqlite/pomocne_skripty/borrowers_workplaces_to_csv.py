import json, csv

with open('../../webScrape/ucitele2.json', 'r') as file:
    borrowers = json.loads(file.readline())

with open('../data/data_Workplaces.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    workplaces = {i[1]: i[0] for i in reader}

borrowers_workplaces = []

with open('../data/data_BorrowersWorkplaces.csv', 'w') as csv_file:
    for borrower in borrowers:
        for workplace in borrower['workplaces']:
            borrowers_workplaces.append((
                borrower['id'],
                workplaces[workplace]
            ))
            csv_file.write(f"{borrower['id']};{workplaces[workplace]}\n")

print(borrowers_workplaces)
