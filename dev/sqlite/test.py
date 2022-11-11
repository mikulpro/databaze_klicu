from db_interface import Db



a = Db.get_rooms_by_floor(1)

print("Results:")
print(dir(a))
print(f"Length: {len(a.keys())}")
for i in a.keys():

    print(i)