titles = (
    ('JUDr.', True, 30),
    ('RNDr.', True, 30),
    ('MUDr.', True, 30),
    ('Bc.', True, 10),
    ('DiS.', False, 0),
    ('ak. mal.', True, 20),
    ('prof.', True, 50),
    ('Ing.', True, 20),
    ('PaedDr.', True, 30),
    ('Ph.D.', False, 0),
    ('doc.', True, 40),
    ('PhD.', False, 0),
    ('CSc.', False, 0),
    ('Mgr.', True, 20),
    ('PhDr.', True, 30),
    ('PharmDr.', True, 30),
    ('DSc.', False, 0),
    ('Dr.', True, 30),
    ('Dr.', False, 0),
    ('DrSc.', False, 0)
 )
new_titles = []
for i in titles:
    new_titles.append((i[0], i[1]))

id = 1
with open(f"../data/data_Titles.csv", "w") as outfile:
    for row in new_titles:
        outfile.write(str(id) + ';')
        for i in range(len(row)):
            outfile.write(str(row[i]))
            if i < (len(row)-1):
                outfile.write(";")
        outfile.write("\n")
        id += 1

print(new_titles)
