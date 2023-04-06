import datetime

from fastapi import FastAPI, HTTPException
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
import bcrypt
from fastapi.middleware.cors import CORSMiddleware

from .db_models import *
from .models import *


SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create the database tables
Base.metadata.create_all(bind=engine)


# Initialize the app
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define the endpoints
# Room Types
@app.post("/room_types/")
def create_room_type(room_type: RoomType, db: Session = Depends(get_db)):
    db_room_type = RoomTypeDB(name=room_type.name)
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type


@app.get("/room_types/")
def read_room_types(db: Session = Depends(get_db)):
    room_types = db.query(RoomTypeDB).all()
    return room_types


@app.put("/room_types/{room_type_id}")
def update_room_type(room_type_id: int, room_type: RoomType, db: Session = Depends(get_db)):
    db_room_type = db.query(RoomTypeDB).filter(RoomTypeDB.id == room_type_id).first()
    if not db_room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    db_room_type.name = room_type.name
    db.commit()
    db.refresh(db_room_type)
    return db_room_type


@app.delete("/room_types/{room_type_id}")
def delete_room_type(room_type_id: int, db: Session = Depends(get_db)):
    db_room_type = db.query(RoomTypeDB).filter(RoomTypeDB.id == room_type_id).first()
    if not db_room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    db.delete(db_room_type)
    db.commit()
    return {"message": "Room type deleted"}


# Faculties
@app.post("/faculties/")
def create_faculty(faculty: Faculty, db: Session = Depends(get_db)):
    db_faculty = FacultyDB(abbreviation=faculty.abbreviation, name=faculty.name)
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty


@app.get("/faculties/")
def read_faculties(db: Session = Depends(get_db)):
    faculties = db.query(FacultyDB).all()
    return faculties


@app.put("/faculties/{faculty_id}")
def update_faculty(faculty_id: int, faculty: Faculty, db: Session = Depends(get_db)):
    db_faculty = db.query(FacultyDB).filter(FacultyDB.id == faculty_id).first()
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    db_faculty.abbreviation = faculty.abbreviation
    db_faculty.name = faculty.name
    db.commit()
    db.refresh(db_faculty)
    return db_faculty


@app.delete("/faculties/{faculty_id}")
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    db_faculty = db.query(FacultyDB).filter(FacultyDB.id == faculty_id).first()
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    db.delete(db_faculty)
    db.commit()
    return {"message": "Faculty deleted"}


# Authorized Persons
@app.post("/authorized_persons/")
def create_authorized_person(authorized_person: AuthorizedPerson, db: Session = Depends(get_db)):
    db_authorized_person = AuthorizedPersonDB(
        firstname=authorized_person.firstname,
        surname=authorized_person.surname,
        workplace_id=authorized_person.workplace_id,
        created=authorized_person.created)
    db.add(db_authorized_person)
    db.commit()
    db.refresh(db_authorized_person)
    return db_authorized_person


@app.get("/authorized_persons/")
def read_authorized_persons(db: Session = Depends(get_db)):
    authorized_persons = db.query(AuthorizedPersonDB).all()
    return authorized_persons


@app.put("/authorized_persons/{authorized_person_id}")
def update_authorized_person(authorized_person_id: int, authorized_person: AuthorizedPerson, db: Session = Depends(get_db)):
    db_authorized_person = db.query(AuthorizedPersonDB).filter(AuthorizedPersonDB.id == authorized_person_id).first()
    if not db_authorized_person:
        raise HTTPException(status_code=404, detail="Authorized person not found")
    db_authorized_person.firstname = authorized_person.firstname
    db_authorized_person.surname = authorized_person.surname
    db_authorized_person.workplace_id = authorized_person.workplace_id
    db_authorized_person.created = authorized_person.created
    db.commit()
    db.refresh(db_authorized_person)
    return db_authorized_person


@app.delete("/authorized_persons/{authorized_person_id}")
def delete_authorized_person(authorized_person_id: int, db: Session = Depends(get_db)):
    db_authorized_person = db.query(AuthorizedPersonDB).filter(AuthorizedPersonDB.id == authorized_person_id).first()
    if not db_authorized_person:
        raise HTTPException(status_code=404, detail="Authorized person not found")
    db.delete(db_authorized_person)
    db.commit()
    return {"message": "Authorized person deleted"}


# Alembic Version
@app.get("/alembic_version/")
def read_alembic_version(db: Session = Depends(get_db)):
    alembic_version = db.query(AlembicVersionDB).all()
    return alembic_version


# Authorization Origins
@app.post("/authorization_origins/")
def create_authorization_origin(authorization_origin: AuthorizationOrigin, db: Session = Depends(get_db)):
    db_authorization_origin = AuthorizationOriginDB(name=authorization_origin.name)
    db.add(db_authorization_origin)
    db.commit()
    db.refresh(db_authorization_origin)
    return db_authorization_origin


@app.get("/authorization_origins/")
def read_authorization_origins(db: Session = Depends(get_db)):
    authorization_origins = db.query(AuthorizationOriginDB).all()
    return authorization_origins


@app.put("/authorization_origins/{authorization_origin_id}")
def update_authorization_origin(authorization_origin_id: int, authorization_origin: AuthorizationOrigin, db: Session = Depends(get_db)):
    db_authorization_origin = db.query(AuthorizationOriginDB).filter(AuthorizationOriginDB.id == authorization_origin_id).first()
    if not db_authorization_origin:
        raise HTTPException(status_code=404, detail="Authorization origin not found")
    db_authorization_origin.name = authorization_origin.name
    db.commit()
    db.refresh(db_authorization_origin)
    return db_authorization_origin


@app.delete("/authorization_origins/{authorization_origin_id}")
def delete_authorization_origin(authorization_origin_id: int, db: Session = Depends(get_db)):
    db_authorization_origin = db.query(AuthorizationOriginDB).filter(AuthorizationOriginDB.id == authorization_origin_id).first()
    if not db_authorization_origin:
        raise HTTPException(status_code=404, detail="Authorization origin not found")
    db.delete(db_authorization_origin)
    db.commit()
    return {"message": "Authorization origin deleted"}


# Workplaces
@app.post("/workplaces/")
def create_workplace(workplace: Workplace, db: Session = Depends(get_db)):
    db_workplace = WorkplaceDB(abbreviation=workplace.abbreviation, name=workplace.name, faculty_id=workplace.faculty_id)
    db.add(db_workplace)
    db.commit()
    db.refresh(db_workplace)
    return db_workplace


@app.get("/workplaces/")
def read_workplaces(db: Session = Depends(get_db)):
    workplaces = db.query(WorkplaceDB).all()
    return workplaces


@app.put("/workplaces/{workplace_id}")
def update_workplace(workplace_id: int, workplace: Workplace, db: Session = Depends(get_db)):
    db_workplace = db.query(WorkplaceDB).filter(WorkplaceDB.id == workplace_id).first()
    if not db_workplace:
        raise HTTPException(status_code=404, detail="Workplace not found")
    db_workplace.abbreviation = workplace.abbreviation
    db_workplace.name = workplace.name
    db_workplace.faculty_id = workplace.faculty_id
    db.commit()
    db.refresh(db_workplace)
    return db_workplace


@app.delete("/workplaces/{workplace_id}")
def delete_workplace(workplace_id: int, db: Session = Depends(get_db)):
    db_workplace = db.query(WorkplaceDB).filter(WorkplaceDB.id == workplace_id).first()
    if not db_workplace:
        raise HTTPException(status_code=404, detail="Workplace not found")
    db.delete(db_workplace)
    db.commit()
    return {"message": "Workplace deleted"}


# Borrowings
@app.post("/borrowings/")
def create_borrowing(borrowing: Borrowing, db: Session = Depends(get_db)):
    db_borrowing = BorrowingDB(key_id=borrowing.key_id, authorization_id=borrowing.authorization_id, borrowed=borrowing.borrowed, returned=borrowing.returned)
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


@app.get("/borrowings/")
def read_borrowings(db: Session = Depends(get_db)):
    borrowings = db.query(BorrowingDB).all()
    return borrowings


@app.put("/borrowings/{borrowing_id}")
def update_borrowing(borrowing_id: int, borrowing: Borrowing, db: Session = Depends(get_db)):
    db_borrowing = db.query(BorrowingDB).filter(BorrowingDB.id == borrowing_id).first()
    if not db_borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    db_borrowing.key_id = borrowing.key_id
    db_borrowing.authorization_id = borrowing.authorization_id
    db_borrowing.borrowed = borrowing.borrowed
    db_borrowing.returned = borrowing.returned
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


@app.delete("/borrowings/{borrowing_id}")
def delete_borrowing(borrowing_id: int, db: Session = Depends(get_db)):
    db_borrowing = db.query(BorrowingDB).filter(BorrowingDB.id == borrowing_id).first()
    if not db_borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    db.delete(db_borrowing)
    db.commit()
    return {"message": "Borrowing deleted"}


# Keys
@app.post("/keys/")
def create_key(key: Key, db: Session = Depends(get_db)):
    db_key = KeyDB(registration_number=key.registration_number, key_class=key.key_class, room_id=key.room_id)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key


@app.get("/keys/")
def read_keys(db: Session = Depends(get_db)):
    keys = db.query(KeyDB).all()
    return keys
@app.put("/keys/{key_id}")
def update_key(key_id: int, key: Key, db: Session = Depends(get_db)):
    db_key = db.query(KeyDB).filter(KeyDB.id == key_id).first()
    if not db_key:
        raise HTTPException(status_code=404, detail="Key not found")
    db_key.registration_number = key.registration_number
    db_key.key_class = key.key_class
    db_key.room_id = key.room_id
    db.commit()
    db.refresh(db_key)
    return db_key


@app.delete("/keys/{key_id}")
def delete_key(key_id: int, db: Session = Depends(get_db)):
    db_key = db.query(KeyDB).filter(KeyDB.id == key_id).first()
    if not db_key:
        raise HTTPException(status_code=404, detail="Key not found")
    db.delete(db_key)
    db.commit()
    return {"message": "Key deleted"}


# Rooms
@app.post("/rooms/")
def create_room(room: Room, db: Session = Depends(get_db)):
    db_room = RoomDB(name=room.name, floor=room.floor, type_id=room.type_id, faculty_id=room.faculty_id, borrowings_count=room.borrowings_count)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@app.get("/rooms/")
def read_rooms(db: Session = Depends(get_db)):
    rooms = db.query(RoomDB).all()
    return rooms


@app.put("/rooms/{room_id}")
def update_room(room_id: int, room: Room, db: Session = Depends(get_db)):
    db_room = db.query(RoomDB).filter(RoomDB.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db_room.name = room.name
    db_room.floor = room.floor
    db_room.type_id = room.type_id
    db_room.faculty_id = room.faculty_id
    db_room.borrowings_count = room.borrowings_count
    db.commit()
    db.refresh(db_room)
    return db_room


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(RoomDB).filter(RoomDB.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"message": "Room deleted"}


# Users
# @app.post("/users/")
# def create_user(user: User, db: Session = Depends(get_db)):
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#     db_user = UserDB(username=user.username, password=hashed_password.decode('utf-8'), is_superuser=user.is_superuser)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return User.from_orm(db_user)


@app.get("/users/")
def read_users(db: Session = Depends(get_db), limit=None):
    users = db.query(UserDB).all()

    return [User.from_orm(user) for user in users]


# @app.put("/users/{user_id}")
# def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
#     db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db_user.username = user.username
#     db_user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#     db_user.is_superuser = user.is_superuser
#     db.commit()
#     db.refresh(db_user)
#     return db_user

@app.post("/authorizations/")
def create_authorization(authorization: Authorization, db: Session = Depends(get_db)):
    db_authorization = AuthorizationDB(
        person_id=authorization.person_id,
        created=datetime.utcnow(),
        expiration=authorization.expiration,
        origin_id=authorization.origin_id,
        room_id=authorization.room_id
    )
    db.add(db_authorization)
    db.commit()
    db.refresh(db_authorization)
    return db_authorization

@app.get("/authorizations/")
def read_authorizations(db: Session = Depends(get_db)):
    authorizations = db.query(AuthorizationDB).all()
    return authorizations

@app.get("/authorizations/{authorization_id}")
def read_authorization(authorization_id: int, db: Session = Depends(get_db)):
    authorization = db.query(AuthorizationDB).filter(AuthorizationDB.id == authorization_id).first()
    if not authorization:
        raise HTTPException(status_code=404, detail="Authorization not found")
    return authorization

@app.put("/authorizations/{authorization_id}")
def update_authorization(authorization_id: int, authorization: Authorization, db: Session = Depends(get_db)):
    db_authorization = db.query(AuthorizationDB).filter(AuthorizationDB.id == authorization_id).first()
    if not db_authorization:
        raise HTTPException(status_code=404, detail="Authorization not found")

    db_authorization.person_id = authorization.person_id
    db_authorization.expiration = authorization.expiration
    db_authorization.origin_id = authorization.origin_id
    db_authorization.room_id = authorization.room_id

    db.commit()
    db.refresh(db_authorization)
    return db_authorization

@app.delete("/authorizations/{authorization_id}")
def delete_authorization(authorization_id: int, db: Session = Depends(get_db)):
    db_authorization = db.query(AuthorizationDB).filter(AuthorizationDB.id == authorization_id).first()
    if not db_authorization:
        raise HTTPException(status_code=404, detail="Authorization not found")

    db.delete(db_authorization)
    db.commit()
    return {"message": "Authorization deleted successfully"}
