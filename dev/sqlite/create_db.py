import pysqlite3

IMPORT_DATA = True

con = pysqlite3.connect("keys_test.db")
cur = con.cursor()

con.execute("""CREATE TABLE RoomTypes(
  id INTEGER PRIMARY KEY ,
  name VARCHAR NOT NULL
  );""")

con.execute("""CREATE TABLE Faculties(
  id INTEGER PRIMARY KEY,
  abbreviation VARCHAR UNIQUE NOT NULL,
  name VARCHAR NOT NULL
);""")

con.execute("""CREATE TABLE Rooms(
  id INTEGER PRIMARY KEY,
  name VARCHAR UNIQUE NOT NULL,
  floor INTEGER NOT NULL,
  type INTEGER,
  faculty INTEGER,
  FOREIGN KEY(type) REFERENCES RoomTypes(id),
  FOREIGN KEY(faculty) REFERENCES Faculties(id)
);""")

con.execute("""CREATE TABLE Keys(
  id INTEGER PRIMARY KEY,
  registration_number INTEGER NOT NULL,
  is_copy INTEGER NOT NULL DEFAULT false 
);""")

con.execute("""CREATE TABLE KeysRooms(
  key INTEGER,
  room INTEGER,
  FOREIGN KEY(key) REFERENCES Keys(registration_number),
  FOREIGN KEY(room) REFERENCES Rooms(id)
);""")

con.execute("""CREATE TABLE Workplaces(
  id INTEGER PRIMARY KEY,
  abbreviation VARCHAR UNIQUE NOT NULL,
  name VARCHAR NOT NULL,
  faculty INTEGER,
  FOREIGN KEY(faculty) REFERENCES Faculties(id)
);""")

con.execute("""CREATE TABLE Borrowers(
  id INTEGER PRIMARY KEY,
  firstname VARCHAR NOT NULL,
  surname VARCHAR NOT NULL,
  id_card VARCHAR
);""")

con.execute("""CREATE TABLE Titles(
  id INTEGER PRIMARY KEY,
  abbreviation VARCHAR NOT NULL ,
  is_before_name INTEGER NOT NULL
);""")

con.execute("""CREATE TABLE BorrowersTitles(
  borrower INTEGER,
  title INTEGER,
  title_order INTEGER NOT NULL,
  FOREIGN KEY(borrower) REFERENCES Borrowers(id), 
  FOREIGN KEY(title) REFERENCES Titiles(id)
);""")

con.execute("""CREATE TABLE BorrowersWorkplaces(
  borrower INTEGER,
  workplace INTEGER,
  FOREIGN KEY(borrower) REFERENCES Borrowers(id),
  FOREIGN KEY(workplace) REFERENCES Workplaces(id)
);""")

con.execute("""CREATE TABLE Doorkeepers(
  id INTEGER PRIMARY KEY,
  firstname VARCHAR NOT NULL,
  surname VARCHAR NOT NULL,
  password VARCHAR
);""")

con.execute("""CREATE TABLE Borrowings(
  id INTEGER PRIMARY KEY,
  key INTEGER,
  borrower INTEGER,
  borrowed TIMESTAMP NOT NULL,
  returned TIMESTAMP INTEGER, 
  doorkeeper INTEGER,
  FOREIGN KEY(key) REFERENCES Keys(id),
  FOREIGN KEY(borrower) REFERENCES Borrowers(id),
  FOREIGN KEY(doorkeeper) REFERENCES Doorkeepers(id)
);""")

print('Databáze byla úspěšně vytvořena')

if IMPORT_DATA:
    import import_data_db
    import_data_db.do_directory('data', con)
    con.commit()

# Close the connection
con.close()
