from typing import List

from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Client, User, Role
from src.schemas import ClientResponse, ClientModel, BirthdayResponse
from src.repository import clients as repository_clients
from src.services.auth import auth_service
from src.services.roles import RolesAccess
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/clients", tags=["Clients"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator])
access_update = RolesAccess([Role.admin, Role.moderator])
access_delete = RolesAccess([Role.admin])


@router.get("/", response_model=List[ClientResponse],
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def get_clients(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    users = await repository_clients.get_clients(limit, offset, db)
    return users


@router.get("/birthday/", response_model=List[BirthdayResponse],
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def get_users_birthday(days: int = Query(7, le=365), db: Session = Depends(get_db),
                             _: User = Depends(auth_service.get_current_user)):
    users = await repository_clients.get_birthday(days, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return users


@router.get("/search/", response_model=List[ClientResponse],
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def search_clients(data: str, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    clients = await repository_clients.search_clients(data, db)
    if clients is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return clients


@router.get("/{client_id}", response_model=ClientResponse,
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def get_user(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                   _: User = Depends(auth_service.get_current_user)):
    client = await repository_clients.get_client(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_create), Depends(RateLimiter(times=2, seconds=60))],
             description="No more than 2 requests per minute")
async def create_users(body: ClientModel, db: Session = Depends(get_db),
                       _: User = Depends(auth_service.get_current_user)):
    client = await repository_clients.get_client_by_email(body.email, db)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client with this email already exist")
    client = await repository_clients.get_client_by_phone(body.phone_number, db)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client with this phone already exist")
    client = await repository_clients.create_client(body, db)
    return client


@router.put("/{client_id}", response_model=ClientResponse,
            dependencies=[Depends(access_update), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def update_user(body: ClientModel, client_id: int = Path(ge=1), db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    client = await repository_clients.update_client(body, client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


@router.delete("/{client_id}", response_model=ClientResponse,
               dependencies=[Depends(access_delete), Depends(RateLimiter(times=3, seconds=10))],
               description="No more than 3 requests per 10 seconds")
async def remove_user(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    client = await repository_clients.remove_client(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client
