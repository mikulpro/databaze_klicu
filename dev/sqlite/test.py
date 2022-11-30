from db_interface import Db


db = Db()
# a = db.get_rooms_by_floor(2)
# b = db.get_all_floors()
# c = db.add_borrowing(8, 1)
# d = db.get_rooms_by_floor(-1)
e = db.get_borrowable_keys_by_floor(-1)
# c = db.get_primary_authorizations_for_room(a[0].id)
# d = db.get_ongoing_borrowings()
#e = db.excel_dump()
#f = db.add_user("admin", "admin", is_superuser=True)
g = db.get_user_by_username("test")

print(g)
print(g.check_password("testovaci"))
g.commit()
# print(a[0].name)
# print("Results:")
# print(dir(a))
# print(f"Type: {type(b)}")
# print(f"Length: {len(a)}")
# print(b)
#for i in e:
    #print(i)


#print(e)