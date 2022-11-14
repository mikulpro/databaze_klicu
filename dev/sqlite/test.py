from db_interface import Db


db = Db()
a = db.get_rooms_by_floor(-1)
b = db.get_all_floors()
c = db.get_primary_authorizations_for_room(a[0].id)
d = db.get_ongoing_borrowings()

print(a[0].name)
print("Results:")
print(dir(a))
print(f"Type: {type(b)}")
print(f"Length: {len(a)}")
for i in c:

    print(len(i.borrowings))
print(b)