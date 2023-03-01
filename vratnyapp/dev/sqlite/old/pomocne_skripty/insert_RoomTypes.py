import pysqlite3


con = pysqlite3.connect("keys_test.db")
cur = con.cursor()

with open('webScrape/types.txt') as file:
    data = file.readline()


# convert string representation of set to list
room_types = [i.replace("'", " ", len(i)).strip() for i in data[1:-1].split(',')]

rt_sql = ""
for room_type in room_types:
    rt_sql += f"('{room_type}'), "
rt_sql = rt_sql[:-2]


statement = """INSERT INTO RoomTypes (name) VALUES %s ;""" % rt_sql
# print("Executed: " + statement)
# con.execute(statement)

statement = "SELECT * FROM RoomTypes;"
cur.execute(statement)

print("Executed: " + statement)
output = cur.fetchall()
for row in output:
    print(row)

con.commit()

# Close the connection
con.close()
