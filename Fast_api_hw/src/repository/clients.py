from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Client
from src.schemas import ClientModel


async def get_clients(limit: int, offset: int, db: Session):
    client = db.query(Client).limit(limit).offset(offset).all()
    return client


async def get_client(client_id: int, db: Session):
    client = db.query(Client).filter_by(id=client_id).first()
    return client


async def get_client_by_email(email: str, db: Session):
    client = db.query(Client).filter_by(email=email).first()
    return client


async def get_client_by_phone(phone_number: str, db: Session):
    client = db.query(Client).filter_by(phone_number=phone_number).first()
    return client


async def create_client(body: ClientModel, db: Session):
    client = Client(**body.dict())
    db.add(client)
    db.commit()
    return client


async def update_client(body: ClientModel, user_id: int, db: Session):
    client = await get_client(user_id, db)
    if client:
        client.firstname = body.firstname
        client.lastname = body.lastname
        client.email = body.email
        client.phone_number = body.phone_number
        client.birthday = body.birthday
        client.additional_data = body.additional_data
        db.add(client)
        db.commit()
    return client


async def remove_client(client_id: int, db: Session):
    client = await get_client(client_id, db)
    if client:
        db.delete(client)
        db.commit()
    return client


async def get_birthday(days: int, db: Session):
    today = datetime.now().date()
    end_period = today + timedelta(days=days)
    client = db.query(Client).all()
    birthday_list = []
    for client in client:
        birthday_this_year = datetime.strptime(client.birthday, "%Y-%m-%d").date().replace(year=2023)
        if end_period >= birthday_this_year >= today:
            birthday_list.append(client)
    return birthday_list


async def search_clients(data: str, db: Session):
    users = db.query(Client).filter(Client.firstname.ilike(f"%{data}%") |
                                    Client.lastname.ilike(f"%{data}%") |
                                    Client.email.ilike(f"%{data}%")).all()
    return users
