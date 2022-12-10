from db_interface import Db


db = Db()

#a = db.update_person(301, surname="Novák1")
#b = db.get_persons_by_name_fraction("Jan Novák")
a = db.get_rooms_availability_dict_by_floor(1)
# c = db.get_valid_authorizations_for_room(1)
# d = db.get_prioritized_authorizations_for_room(1)
# for i in c:
#     print(i.name)
# print(len(c))
# print(len(d))
# print(c)
# print(d)
# for i in c:
#     if i.person_id == 120:
#         #print(i)
#         pass
#     if i.person_id == 23:
#         a = i.person.borrowings
#         print("Borro 23")
#         print(len(a))
# i.person.borrowings
#/home/doctordehi/dev/skola/databaze_klicu/dev/sqlite/db_interface.py:118: SAWarning: relationship 'AuthorizedPerson.borrowings' will copy column authorized_persons.id to column authorizations.person_id, which conflicts with relationship(s): 'AuthorizedPerson.authorizations' (copies authorized_persons.id to authorizations.person_id). If this is not the intention, consider if these relationships should be linked with back_populates, or if viewonly=True should be applied to one or more if they are read-only. For the less common case that foreign key constraints are partially overlapping, the orm.foreign() annotation can be used to isolate the columns that should be written towards.   To silence this warning, add the parameter 'overlaps="authorizations"' to the 'AuthorizedPerson.borrowings' relationship. (Background on this error at: https://sqlalche.me/e/14/qzyx)


#print(b)
# keys = []
# for i in a:
#     if i.get_ordinary_key() is None:
#         keys.append(i)
#
# print("Problémy:" + str(keys))
# key_id = 20
# db.add_borrowing(key_id, 1747)
# db.add_borrowing(key_id, 1585)
# db.add_borrowing(key_id, 698)
# db.add_borrowing(key_id, 698)


