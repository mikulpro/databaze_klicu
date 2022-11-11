from models import *
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import Session
# from sqlalchemy.sql import select
import datetime

"""
Db:
    get_all_floors(self) -> list[int]
    get_rooms_by_floor(self, int: floor) -> list[Room]
    get_primary_authorizations_for_room(self, int: room_id)-> list[Authorizations]
    get_primary_authorizations_for_room(self, int: room_id) -> list[Authorizations]
    get_borrowers_by_name_fraction(self, str: fraction) -> list[AuthorizedPerson]
    get_room_by_name_fraction(self, str: fraction, int: floor=None) -> list[Room]
    
    add_borrowing(self, int: key_id, int: borrower_id)
    return_key(self, int: borrowing_id)
    get_ongoing_borrowings(self) -> list[Borrowing]
    
    excel_dump(self) -> list[list[str]]
"""


class Db:

    def __int__(self, db_path="sqlite:///db.sqlite"):
        engine = create_engine(db_path, echo=True, future=True)
        # Base.metadata.create_all(engine)
        self.session = Session(engine)

    def get_all_floors(self):
        return self.session.query(Room).distinct(Room.floor)

    def get_rooms_by_floor(self, floor):
        # return self.session.execute(select(Room).filter(Room.floor == floor))
        return self.session.query(Room).filter(Room.floor == floor)

    def get_authorizations_for_room(self, room_id):
        room = self.session.query(Room).filter(Room.id == room_id)
        return room.authorizations.filter(Authorization.expiration > datetime.datetime.utcnow)

    def get_primary_authorizations_for_room(self, room_id):
        authorizations = self.get_authorizations_for_room(room_id)
        # přidat filtorvání na základě origin
        return authorizations

    def get_borrowers_by_name_fraction(self, fraction):
        fractions = fraction.split(" ")

        if len(fractions) == 1:
            return self.session.query(AuthorizedPerson).filter(
                or_(AuthorizedPerson.firstname.like(f"{fractions[0]}%"),
                    AuthorizedPerson.surname.like(f"{fractions[0]}%")
                    ))
        elif len(fractions) == 2:
            return self.session.query(AuthorizedPerson).filter(
                or_(
                    and_(AuthorizedPerson.firstname.like(f"{fractions[0]}%"),
                         AuthorizedPerson.surname.like(f"{fractions[1]}%"),
                         ),
                    and_(AuthorizedPerson.firstname.like(f"{fractions[1]}%"),
                         AuthorizedPerson.surname.like(f"{fractions[0]}%"),
                         ),
                ))
        else:
            return []

    def get_room_by_name_fraction(self, fraction, floor=None):
        if floor:
            return self.session.query(Room).filter(Room.name.like(f"%{fraction}%"), Room.floor == floor)
        else:
            return self.session.query(Room).filter(Room.name.like(f"%{fraction}%"))

    def add_borrowing(self, key_id, borrower_id):
        borrowing = Borrowing(key_id=key_id, borrower_id=borrower_id)
        self.session.add(borrowing)

    def return_key(self, borrowing_id):
        borrowing = self.session.query(Borrowing).filter(Borrowing.id == borrowing_id).one()
        borrowing.return_key()

    def get_ongoing_borrowings(self):
        return self.session.query(Borrowing).filter(Borrowing.returned.is_(None))

    def excel_dump(self):
        # [borrowed: date, time, key, borrower name, return: date, time]
        data = []
        borrowings = self.session.query(Borrowing)
        for borrowing in borrowings:
            row = [
                borrowing.borrowed.strftime("%d.%m.%Y"),
                borrowing.borrowed.strftime("%H:%M"),
                str(borrowing.key.registration_number),
                borrowing.borrower.borrower.get_full_name(),
            ]
            if borrowing.returned:
                row.extend([
                    borrowing.returned.strftime("%d.%m.%Y"),
                    borrowing.returned.strftime("%H:%M"),
                ])
            else:
                row.extend([
                    "",
                    ""
                ])

            data.append(row)

        return data
