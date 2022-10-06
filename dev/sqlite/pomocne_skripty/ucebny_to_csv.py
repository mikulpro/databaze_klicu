import json
import csv

with open('../data/data_RoomTypes.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    room_types = {i[1]: i[0] for i in reader}
    print(room_types)

with open('../data/data_Faculties.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    faculties = {i[1]: i[0] for i in reader}
    print(faculties)

faculties.update({'PRF': 1, 'FZP': 2})

with open("../../webScrape/ucebny.json") as file:
    data = file.readline()

ucebny_dict = json.loads(data)
ucebny_out = []

id = 1
for floor in ucebny_dict.keys():
    for ucebna in ucebny_dict[floor]:
        # name, floor, type, faculty
        ucebny_out.append((
            id,
            ucebna['name'],
            floor,
            room_types[ucebna['type']],
            faculties[ucebna['faculty']]
        ))
        id += 1


with open(f"../data/export_Rooms.csv", "w") as outfile:
    for row in ucebny_out:
        for i in range(len(row)):
            outfile.write(str(row[i]))
            if i < (len(row)-1):
                outfile.write(";")
        outfile.write("\n")

print(ucebny_out)

