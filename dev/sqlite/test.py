from db_interface import Db


db = Db()
a = db.get_rooms_by_floor(-1)
b = db.get_all_floors()


print("Results:")
print(dir(a))
print(f"Type: {type(b)}")
print(f"Length: {len(a)}")
for i in a:

    print(i)
print(b)