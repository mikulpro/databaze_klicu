from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

import datetime


Base = declarative_base()


# keys_rooms = Table(
#     "keys_rooms",
#     Base.metadata,
#     Column("key_number", ForeignKey("keys.registration_number")),
#     Column("room_id", ForeignKey("rooms.id")),
# )
#
# authorizations_rooms = Table(
#     "authorizations_rooms",
#     Base.metadata,
#     Column("authorization_id", ForeignKey("authorizations.id")),
#     Column("room_id", ForeignKey("rooms.id")),
#
# )


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True)
    key_id = Column(Integer, ForeignKey("keys.id"), nullable=False)
    key = relationship("Key", back_populates="borrowings")
    authorization_id = Column(Integer, ForeignKey("authorizations.id"), nullable=False)
    authorization = relationship("Authorization", back_populates="borrowings")
    borrowed = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    returned = Column(DateTime(timezone=True), nullable=True)

    def return_key(self):
        self.returned = datetime.datetime.utcnow()

    def __repr__(self):
        return f"Borrowing(id={self.id}, key={self.key}, borrower={self.authorization}, borrowed={self.borrowed} returned={self.returned}"


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True)
    registration_number = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    room = relationship("Room", back_populates="keys")
    key_class = Column(Integer, default=0)
    borrowings = relationship("Borrowing", back_populates="key")

    def is_borrowed(self):
        for borrowing in self.borrowings:
            if not borrowing.returned:
                return True
            else:
                return False


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(8), nullable=False, unique=True)
    floor = Column(Integer, nullable=False)
    type_id = Column(Integer, ForeignKey("room_types.id"))
    type = relationship("RoomType")
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty")
    authorizations = relationship("Authorization", back_populates="room")
    keys = relationship("Key", back_populates="room")
    borrowings_count = Column(Integer, nullable=False, default=0)

    def get_common_key(self):
        for key in self.keys:
            if key.key_class == 0:
                if not key.is_borrowed():
                    return key

    def increment_borrowings_count(self):
        if not self.borrowings_count:
            self.borrowings_count = 0
        self.borrowings_count += 1



class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True)
    abbreviation = Column(String(4), nullable=False, unique=True)
    name = Column(String(64), nullable=False, unique=True)


class AuthorizedPerson(Base):
    __tablename__ = "authorized_persons"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    workplace_id = Column(Integer, ForeignKey("workplaces.id"))
    workplace = relationship("Workplace")
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    authorizations = relationship("Authorization", back_populates="person")

    def get_full_name(self):
        return self.firstname + " " + self.surname


class Workplace(Base):
    __tablename__ = "workplaces"

    id = Column(Integer, primary_key=True)
    abbreviation = Column(String(8), nullable=False, unique=True)
    name = Column(String(64), nullable=False, unique=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty")


class Authorization(Base):
    __tablename__ = "authorizations"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("authorized_persons.id"))
    person = relationship("AuthorizedPerson")
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    room = relationship("Room", back_populates="authorizations")
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    expiration = Column(DateTime(timezone=True), nullable=False)
    origin_id = Column(Integer, ForeignKey("authorization_origins.id"), nullable=False)
    origin = relationship("AuthorizationOrigin")

    borrowings = relationship("Borrowing", back_populates="authorization")
    borrowings_count = Column(Integer, nullable=False, default=0)

    def increment_borrowings_count(self):
        if not self.borrowings_count:
            self.borrowings_count = 0
        self.borrowings_count += 1


class AuthorizationOrigin(Base):
    __tablename__ = "authorization_origins"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
