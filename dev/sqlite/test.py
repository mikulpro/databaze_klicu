from db_interface import Db


db = Db()

a = db.get_all_rooms()

keys = []
for i in a:
    if i.get_ordinary_key() is None:
        keys.append(i)

print("Problémy:" + str(keys))

