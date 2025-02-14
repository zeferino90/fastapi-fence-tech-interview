from contextlib import asynccontextmanager

from typing import Annotated

from fastapi import FastAPI, Depends

from sqlalchemy import event
from fastapi.requests import Request
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from database.database_creation import engine, SessionLocal
from database.models import Item, AuditLog, create_db_and_tables
from schemas import ItemPostSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


# This listener is good to audit what happens in the database but for auditing the API requests,
# we need to use middleware.
def audit_listener(mapper, connection, target):
    with Session(bind=connection) as session:
        log_entry = AuditLog(
            table_name=target.__tablename__,
            record_id=target.id,
            user_id=1,
            action="INSERT",
            new_value=str(target.__dict__),
        )
        session.add(log_entry)
        session.commit()

event.listen(Item, "after_insert", audit_listener)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.get("/items/{item_id}")
def get_item(item_id: str, session: Session = Depends(get_db)) -> Item:
    result = session.exec(select(Item).where(Item.id == item_id)).first()
    return Item(name=item_id)


@app.get("/items/")
def get_items(session: Session = Depends(get_db)) -> list[Item]:
    result = session.exec(select(Item)).all()
    return result


@app.post("/items/", status_code=201)
def create_item(item: Item, session: Session = Depends(get_db)) -> Item:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/audit_log/")
def get_audit_log(session: Session = Depends(get_db)) -> list[Annotated[AuditLog, {"exclude": True}]] :
    result = session.execute(select(AuditLog)).scalars()
    return result
