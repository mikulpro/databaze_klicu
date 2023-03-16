from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Define the database tables
class RoomTypeDB(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(16), nullable=False)


class FacultyDB(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String(4), nullable=False, unique=True)
    name = Column(String(64), nullable=False, unique=True)

    workplaces = relationship("WorkplaceDB", back_populates="faculty")


class AuthorizedPersonDB(Base):
    __tablename__ = "authorized_persons"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    workplace_id = Column(Integer, ForeignKey("workplaces.id"))
    created = Column(DateTime)

    workplace = relationship("WorkplaceDB", back_populates="authorized_persons")


class AlembicVersionDB(Base):
    __tablename__ = "alembic_version"

    version_num = Column(String(32), primary_key=True)


class AuthorizationOriginDB(Base):
    __tablename__ = "authorization_origins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), nullable=False, unique=True)

    authorizations = relationship("AuthorizationDB", back_populates="origin")


class WorkplaceDB(Base):
    __tablename__ = "workplaces"

    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String(8), nullable=False, unique=True)
    name = Column(String(64), nullable=False, unique=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("FacultyDB", back_populates="workplaces")
    authorized_persons = relationship("AuthorizedPersonDB", back_populates="workplace")


class BorrowingDB(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    key_id = Column(Integer, ForeignKey("keys.id"))
    authorization_id = Column(Integer, ForeignKey("authorizations.id"))
    borrowed = Column(DateTime)
    returned = Column(DateTime)
    key = relationship("KeyDB", back_populates="borrowings")
    authorization = relationship("AuthorizationDB", back_populates="borrowings")


class KeyDB(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(Integer, nullable=False)
    key_class = Column(Integer)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("RoomDB", back_populates="keys")
    borrowings = relationship("BorrowingDB", back_populates="key")


class RoomDB(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(8), nullable=False, unique=True)
    floor = Column(Integer, nullable=False)
    type_id = Column(Integer, ForeignKey("room_types.id"))
    type = relationship("RoomTypeDB")
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("FacultyDB")
    borrowings_count = Column(Integer, nullable=False, default=0)
    keys = relationship("KeyDB", back_populates="room")

    authorizations = relationship("AuthorizationDB", back_populates="room")


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String)
    is_superuser = Column(Integer, nullable=False, default=0)


class AuthorizationDB(Base):
    __tablename__ = "authorizations"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("authorized_persons.id"))
    created = Column(DateTime)
    expiration = Column(DateTime, nullable=False)
    origin_id = Column(Integer, ForeignKey("authorization_origins.id"))
    origin = relationship("AuthorizationOriginDB", back_populates="authorizations")
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("RoomDB", back_populates="authorizations")
    borrowings = relationship("BorrowingDB", back_populates="authorization")
