from sqlalchemy import create_engine, or_, and_, update
from sqlalchemy.orm import Session
import sqlalchemy.exc

from dev.sqlite.models import *
from dev.sqlite.utils import hash_func

"""
Db:
    ALL PURPOSE
    get_all_floors(self) -> list[int]
    get_all_rooms(self) -> list[Room]
    get_rooms_by_floor(self, floor: int) -> list[Room]
    get_all_keys(self) -> list[Key]
    get_borrowable_keys_by_floor(self, floor: int, only_ordinary=True: bool) -> list[Key]
    get_available_rooms_by_floor(self, floor: int, only_ordinary=True: bool) -> list[Room]
    get_rooms_availability_dict_by_floor(self, floor: int, only_ordinary=True: bool) -> dict{str: List[Room]} 
    get_valid_authorizations_for_room(self, room_id: int)-> list[Authorization]
    get_prioritized_authorizations_for_room(self, room_id: int) -> list[Authorization]
    
    KEY BORROWING
    add_borrowing(self, int: key_id, int: borrower_id) -> None
    return_key(self, int: borrowing_id) -> None
    get_ongoing_borrowings(self) -> list[Borrowing]
    
    EXCEL GENERATING
    excel_dump(self) -> list[list[str]]
    
    LOGIN SYSTEM
    add_user(username: str, password: str, is_superuser=False: bool) -> None
    get_user_by_username(username: str) -> User?
    
    ADMIN
    add_authorization(person_id: int, room_id: int, expiration: datetime, origin_id=1 : int) -> None
    invalidate_authorization(authorization_id: int) -> None
    invalidate_authorization_obj(authorization: Authorization) -> None
    add_person(self, firstname: str, surname: str, workplace_id=None: int) -> None
    update_person(self, person_id : int, **kwargs) -> None (firstname : str, surname: str, workplace_id : int)
        ?update_authorization(...)
        ?add_key(...)
        ?update_key(..)
        ?add_room(...)
        ?update_room(...)

    get_authorizations_by_name_fraction(self, fraction: str) -> list[Authorization]
    get_persons_by_name_fraction(self, fraction: str) -> list[AuthorizedPerson]
    get_room_by_name_fraction(self, fraction: str, floor=None: int) -> list[Room]
    get_all_authorizations(self) -> list[Authorization]
    get_all_authorized_persons(self) -> list[AuthorizedPerson]
"""


class Db:

    def __init__(self, db_path="sqlite:///db.sqlite"):
        self.db_path = db_path
        self.session = None
        self.new_session()

    def new_session(self):
        engine = create_engine(self.db_path, echo=True, future=True)
        self.session = Session(engine)

    def commit_session(self):
        self.session.commit()

    # ALL PURPOSE
    def get_all_floors(self):
        result = self.session.query(Room.floor).distinct(Room.floor).order_by(Room.floor).all()
        return [i[0] for i in result]

    def get_all_rooms(self):
        return self.session.query(Room).all()

    def get_rooms_by_floor(self, floor):
        rooms = self.session.query(Room).filter(Room.floor == floor).order_by(Room.borrowings_count.desc()).all()
        return rooms

    def get_all_keys(self):
        return self.session.query(Key).all()

    def get_borrowable_keys_by_floor(self, floor, only_ordinary=True):
        q = self.session.query(Key).\
            except_(self.session.query(Key).join(Borrowing).filter(Borrowing.returned == None)).\
            join(Room).filter(Room.floor == floor).\
            order_by(Room.borrowings_count.desc())
        if only_ordinary:
            q = q.filter(Key.key_class == 0)
        keys = q.all()
        return keys

    def get_available_rooms_by_floor(self, floor, only_ordinary=True):
        q_unavailable_rooms = self.session.query(Room).join(Key).join(Borrowing).filter(Borrowing.returned == None)
        q = self.session.query(Room).\
            filter(Room.floor==floor). \
            except_(q_unavailable_rooms).join(Key).\
            order_by(Room.borrowings_count.desc())
        if only_ordinary:
            q = q.filter(Key.key_class == 0)
        rooms = q.all()
        return rooms


    def get_rooms_availability_dict_by_floor(self, floor, only_ordinary=True):
        q_unavailable_rooms = self.session.query(Room).join(Key).join(Borrowing).\
            filter(Borrowing.returned == None, Room.floor==floor)
        q_available_rooms = self.session.query(Room). \
            filter(Room.floor == floor). \
            except_(q_unavailable_rooms).join(Key). \
            order_by(Room.borrowings_count.desc())
        if only_ordinary:
            q_available_rooms = q_available_rooms.filter(Key.key_class == 0)
        available_rooms = q_available_rooms.all()
        unavailable_rooms = q_unavailable_rooms.all()
        return {"available": available_rooms, "unavailable": unavailable_rooms}

    def get_valid_authorizations_for_room(self, room_id):
        authorizations = self.session.query(Authorization).join(Authorization.room).filter(
            Room.id == room_id, Authorization.expiration > datetime.datetime.utcnow()
        ).order_by(Authorization.borrowings_count.desc()).all()
        return sorted(authorizations, key=lambda authorization: len(authorization.borrowings))

    def get_prioritized_authorizations_for_room(self, room_id):
        authorizations = self.get_valid_authorizations_for_room(room_id)
        # přidat filtrování na základě origin
        return authorizations

    # KEY BORROWING
    def add_borrowing(self, key_id, authorization_id):
        borrowing = Borrowing(key_id=key_id, authorization_id=authorization_id)
        self.session.add(borrowing)
        authorization = self.session.query(Authorization).filter(Authorization.id == authorization_id).one()
        authorization.increment_borrowings_count()
        authorization.room.increment_borrowings_count()
        self.session.commit()

    def return_key(self, borrowing_id):
        borrowing = self.session.query(Borrowing).filter(Borrowing.id == borrowing_id).one()
        borrowing.return_key()
        self.session.commit()

    def get_ongoing_borrowings(self):
        return self.session.query(Borrowing).filter(Borrowing.returned.is_(None)).order_by(Borrowing.borrowed).all()

    # EXCEL GENERATING
    def excel_dump(self):
        # [borrowed: date, time, key, borrower name, return: date, time]
        data = []
        borrowings = self.session.query(Borrowing).all()
        for borrowing in borrowings:
            row = [
                borrowing.borrowed.strftime("%d.%m.%Y"),
                borrowing.borrowed.strftime("%H:%M"),
                str(borrowing.key.registration_number),
                borrowing.authorization.person.get_full_name(),
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

    # LOGIN SYSTEM
    def add_user(self, username, password, is_superuser=False):
        password_hash = hash_func(password)
        user = User(username=username, password=password_hash, is_superuser=is_superuser)
        try:
            self.session.add(user)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise Exception("Uživatel s tímto uživatelským jménem již existuje!")

    def get_user_by_username(self, username):
        user = self.session.query(User).filter(User.username == username).one_or_none()
        return user

    # ADMIN
    def add_authorization(self, person_id, room_id, expiration, origin_id=1):
        authorization = Authorization(
            person_id=person_id,
            room_id=room_id,
            expiration=expiration,
            origin_id=origin_id
        )
        self.session.add(authorization)
        self.session.commit()

    def invalidate_authorization(self, authorization_id):
        authorization = self.session.query(Authorization).filter(Authorization.id == authorization_id).one()
        authorization.invalidate()
        self.session.commit()

    def invalidate_authorization_obj(self, authorization):
        authorization.invalidate()
        self.session.commit()

    def add_person(self, firstname, surname, workplace_id=None):
        person = AuthorizedPerson(
            firstname=firstname,
            surname=surname,
            workplace_id=workplace_id
        )
        self.session.add(person)
        self.session.commit()

    def update_person(self, person_id, **kwargs):
        self.session.execute(
            update(AuthorizedPerson)
            .where(AuthorizedPerson.id == person_id)
            .values(kwargs)
        )
        self.session.commit()

    def get_authorizations_by_name_fraction(self, fraction):
        fractions = fraction.split(" ")

        if len(fractions) == 1:
            result_q = self.session.query(Authorization).join(AuthorizedPerson).filter(
                or_(AuthorizedPerson.firstname.like(f"{fractions[0]}%"),
                    AuthorizedPerson.surname.like(f"{fractions[0]}%")
                    ))
        elif len(fractions) == 2:
            result_q = self.session.query(Authorization).join(AuthorizedPerson).filter(
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

        return result_q.order_by(AuthorizedPerson.surname).all()

    def get_persons_by_name_fraction(self, fraction):
        fractions = fraction.split(" ")

        if len(fractions) == 1:
            result_q = self.session.query(AuthorizedPerson).filter(
                or_(AuthorizedPerson.firstname.like(f"{fractions[0]}%"),
                    AuthorizedPerson.surname.like(f"{fractions[0]}%")
                    ))
        elif len(fractions) == 2:
            result_q = self.session.query(AuthorizedPerson).filter(
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

        return result_q.order_by(AuthorizedPerson.surname).all()

    def get_room_by_name_fraction(self, fraction, floor=None):
        rooms_q = self.session.query(Room).filter(Room.name.like(f"%{fraction}%")).order_by(Room.name)
        if floor:
            rooms_q = rooms_q.filter(Room.floor == floor)
        return rooms_q.all()

    def get_all_authorizations(self):
        return self.session.query(Authorization).filter(Authorization.origin_id==1).all()
    def get_all_authorized_persons(self):
        return self.session.query(AuthorizedPerson).all()

