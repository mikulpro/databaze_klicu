from db_interface import Db


db = Db()

#a = db.update_person(301, surname="Novák1")
b = db.get_persons_by_name_fraction("Jan Novák")

print(b)
# keys = []
# for i in a:
#     if i.get_ordinary_key() is None:
#         keys.append(i)
#
# print("Problémy:" + str(keys))

