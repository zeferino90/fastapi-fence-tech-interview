from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import event
from fastapi.requests import Request

from database.database_creation import SessionLocal
from database.models import Item, AuditLog, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


def get_current_user_id(request: Request):
    user = request.state.user  # Not sure if user is here
    return user.id if user else None


def audit_listener(mapper, connection, target):
    session = SessionLocal()
    log_entry = AuditLog(
        table_name=target.__tablename__,
        record_id=target.id,
        user_id=get_current_user_id(),
        action="INSERT",
        new_value=str(target.__dict__)
    )
    session.add(log_entry)
    session.commit()

event.listen(Item, "after_insert", audit_listener)

def get_db(request: Request):
    return request.state.db


@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.get("/items/{item_id}")
def get_item(item_id: str):
    return Item(name=item_id)


@app.get("/items/")
def get_items():
    return []


@app.post("/items/", status_code=201)
def create_item(item: Item):
    return item
