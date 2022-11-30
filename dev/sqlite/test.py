from db_interface import Db


db = Db()

a = db.get_room_by_name_fraction("14", 7)

for i in a:
    print(i.name)
