import pysqlite3


"""
    -get_borrowers_full_names(keyword)
    -get floors
    -get all borrowers
        get all rooms
    -get all rooms on a floor
    -search borrower by name fraction
        search room by name fraction
    excel dump
    
    add vypůjčka - pujc klic
    vrať klíč
    
    add borrower
"""


class Db:
    def __init__(self, db_file):
        self.conn = pysqlite3.connect(db_file)
        self.conn.row_factory = pysqlite3.Row
        self.cur = self.conn.cursor()

    def renew_cursor(self):
        self.cur = self.conn.cursor()

    def search_borrowers_by_fullname_fraction(self, fraction):
        self.cur.execute(f"""SELECT borrower_id as id, full_name 
            FROM borrowers_fullnames 
            WHERE full_name LIKE "%{fraction}%" 
            COLLATE NOCASE
        ;""")
        return self.cur.fetchall()

    def get_all_floors(self):
        self.cur.execute("""SELECT DISTINCT floor FROM Rooms;""")
        return self.cur.fetchall()

    def get_all_borrowers(self):
        self.cur.execute("""SELECT id, firstname, surname 
        FROM Borrowers;""")
        return self.cur.fetchall()

    def get_all_borrowers_fullnames(self):
        self.cur.execute("""SELECT borrower_id as id, full_name 
            FROM borrowers_fullnames;""")
        return self.cur.fetchall()

    def filter_rooms_by_floor(self, floor):
        self.cur.execute(f"""SELECT Rooms.id as id, Rooms.name as name, rt.name as room_type, f.name as faculty
            FROM Rooms 
            LEFT JOIN RoomTypes rt on rt.id == Rooms.type
            LEFT JOIN Faculties f on f.id == Rooms.faculty 
            WHERE floor == {floor};""")
        return self.cur.fetchall()

    def excel_dump(self):
        self.cur.execute("SELECT _ FROM Borrowings")


if __name__ == "__main__":#
    db = Db("../../../db_old.sqlite")
    data = db.filter_rooms_by_floor(5)
    for i in data:
        print(dict(i))
