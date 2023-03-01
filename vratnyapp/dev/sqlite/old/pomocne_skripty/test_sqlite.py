import pysqlite3

con = pysqlite3.connect("test.db")
cursor_obj = con.cursor()

# con.execute("""CREATE TABLE TEST4(
#     id integer primary key,
#   name varchar(4),
#   num int
#   );""")

# con.execute("""CREATE TABLE KEYS(
#   id INTEGER PRIMARY KEY,
#   registration_number INTEGER NOT NULL,
#   is_copy INTEGER NOT NULL DEFAULT false
# );""")

# con.execute("ALTER TABLE KEYS ADD  COLUMN is_copy INTEGER NOT NULL  DEFAULT true;")

# con.execute("""ALTER TABLE TEST3 add COLUMN num tinyint; """)
con.execute("""INSERT into keys(registration_number) values (8284248652);""")
cursor_obj.execute("""select * from keys;""")
output = cursor_obj.fetchall()
print(cursor_obj.description)
for row in output:
    print(row)
print(len(output))

# con.execute(
#      """INSERT INTO TEST (name, timestamp, num) VALUES ("dkekdoeddke", unixepoch(), -24)""")
# con.execute(
#     """INSERT INTO GEEK (Email,Name,Score) VALUES ("geekk2@gmail.com","Geek2",15)""")
# con.execute(
#     """INSERT INTO GEEK (Email,Name,Score) VALUES ("geekk3@gmail.com","Geek3",36)""")
# con.execute(
#     """INSERT INTO GEEK (Email,Name,Score) VALUES ("geekk4@gmail.com","Geek4",27)""")
# con.execute(
#     """INSERT INTO GEEK (Email,Name,Score) VALUES ("geekk5@gmail.com","Geek5",40)""")
# con.execute(
#     """INSERT INTO GEEK (Email,Name,Score) VALUES ("geekk6@gmail.com","Geek6",36)""")
# con.execute(
#     """INSERT INTO GEEK (Email,Name,Score) VALUES ("geekk7@gmail.com","Geek7",27)""")

con.commit()

# Close the connection
con.close()
