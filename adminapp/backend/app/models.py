from pydantic import BaseModel
from typing import Optional


# Define the models
class RoomType(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        orm_mode = True


class Faculty(BaseModel):
    id: Optional[int] = None
    abbreviation: str
    name: str

    class Config:
        orm_mode = True


class AuthorizedPerson(BaseModel):
    id: Optional[int] = None
    firstname: str
    surname: str
    workplace_id: Optional[int] = None
    created: Optional[str] = None

    class Config:
        orm_mode = True


class AlembicVersion(BaseModel):
    version_num: str

    class Config:
        orm_mode = True


class AuthorizationOrigin(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        orm_mode = True


class Workplace(BaseModel):
    id: Optional[int] = None
    abbreviation: str
    name: str
    faculty_id: Optional[int] = None

    class Config:
        orm_mode = True


class Borrowing(BaseModel):
    id: Optional[int] = None
    key_id: int
    authorization_id: int
    borrowed: Optional[str] = None
    returned: Optional[str] = None

    class Config:
        orm_mode = True


class Key(BaseModel):
    id: Optional[int] = None
    registration_number: int
    key_class: Optional[int] = None
    room_id: int

    class Config:
        orm_mode = True


class Room(BaseModel):
    id: Optional[int] = None
    name: str
    floor: int
    type_id: Optional[int] = None
    faculty_id: Optional[int] = None
    borrowings_count: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: Optional[int] = None
    username: str
    #password: Optional[str] = None
    is_superuser: bool

    class Config:
        orm_mode = True
        #exclude = ("password",)


class Authorization(BaseModel):
    id: Optional[int] = None
    person_id: Optional[int] = None
    created: Optional[str] = None
    expiration: str
    origin_id: int
    room_id: int

    class Config:
        orm_mode = True
