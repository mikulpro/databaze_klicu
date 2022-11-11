from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
import datetime

engine = create_engine("sqlite:///db.sqlite", echo=True, future=True)
Base.metadata.create_all(engine, checkfirst=False)
session = Session(engine)

prf = Faculty(abbreviation="PřF", name="Přírodovědecká fakulta")
fzp = Faculty(abbreviation="FŽP", name="Fakulta životního prostředí")

session.add(prf)
session.add(fzp)
session.commit()

a = session.query(Faculty).all()

for i in a:
    print(i.name)
