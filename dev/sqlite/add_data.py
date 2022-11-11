from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
import datetime

engine = create_engine("sqlite:///db.sqlite", echo=True, future=True)
Base.metadata.create_all(engine)
session = Session(engine)

# Faculties
# prf = Faculty(abbreviation="PřF", name="Přírodovědecká fakulta")
# fzp = Faculty(abbreviation="FŽP", name="Fakulta životního prostředí")
#
# session.add(prf)
# session.add(fzp)
# session.commit()
#
# a = session.query(Faculty).all()
#
# for i in a:
#     print(i.name)

# # RoomTypes
# with open("old/data/data_RoomTypes.csv") as f:
#     for row in f.readlines():
#         if row:
#             name = row.strip().split(';')[1]
#             print(name)
#             session.add(RoomType(name=name))
#
# # Rooms
# with open("old/data/data_Rooms.csv") as f:
#     for row in f.readlines():
#         if row:
#             data = row.strip().split(';')
#             name = data[1]
#             floor = data[2]
#             roomtype = data[3]
#             faculty = data[4]
#             print(name)
#             session.add(Room(name=name, floor=floor, type_id=roomtype, faculty_id=faculty))
#
# session.commit()
