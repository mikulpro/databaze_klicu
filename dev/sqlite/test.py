from db_interface import Db


db = Db()

a = db.get_all_rooms()

keys = []
for i in a:
    keys.append(i.get_ordinary_key())
    if i.get_ordinary_key() is None:
        print("Velký problém")


