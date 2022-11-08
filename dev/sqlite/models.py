from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

import datetime


Base = declarative_base()


keys_rooms = Table(
    "keys_rooms",
    Base.metadata,
    Column("key_number", ForeignKey("keys.registration_number")),
    Column("room_id", ForeignKey("rooms.id")),
)

authorizations_rooms = Table(
    "authorizations_rooms",
    Base.metadata,
    Column("authorization_id", ForeignKey("authorizations.id")),
    Column("room_id", ForeignKey("rooms.id")),

)


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True)
    key = relationship("Key", back_populates="borrowings")
    borrower = relationship("Authorization", back_populates="borrowings")
    borrowed = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    returned = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"Borrowing(id={self.id}, key={self.key}, borrower={self.borrower}, borrowed={self.borrowed} returned={self.returned}"


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True)
    registration_number = Column(Integer, nullable=False)
    key_class = Column(Integer, default=0)
    rooms = relationship("Room", secondary=keys_rooms)


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(8), nullable=False)
    floor = Column(Integer, nullable=False)
    type = relationship("RoomType", back_populates="rooms")
    faculty = relationship("Faculty", back_populates="rooms")


class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True)
    abbreviation = Column(String(4), nullable=False)
    name = Column(String(64), nullable=False)


class Authorization(Base):
    __tablename__ = "authorizations"

    id = Column(Integer, primary_key=True)
    borrower = relationship("AuthorizedPerson", back_populates="authorizations")
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    expiration = Column(DateTime(timezone=True), nullable=False)
    origin = relationship("AuthorizationOrigin", back_populates="authorizations")
    rooms = relationship("Rooms", secondary=authorizations_rooms)


class AuthorizationOrigin(Base):
    __tablename__ = "authorization_origins"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)


class AuthorizedPerson(Base):
    __tablename__ = "authorized_persons"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    workplace = relationship("Workplace", back_populates="authorized_persons")
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class WorkPlace(Base):
    __tablename__ = "workplaces"

    id = Column(Integer, primary_key=True)
    abbreviation = Column(String(8), nullable=False)
    name = Column(String(64), nullable=False)
    faculty = relationship("Faculty", back_populates="workplaces")

