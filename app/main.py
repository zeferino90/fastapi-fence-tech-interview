from contextlib import asynccontextmanager

from typing import Annotated

from fastapi import FastAPI, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlmodel import Session, select
from starlette import status
from starlette.exceptions import HTTPException

from database.db_session import get_db
from database.models import Item, AuditLog, create_db_and_tables
from helpers.auth import authenticate_user, create_access_token, get_current_user, oauth2_scheme
from helpers.middleware import AuditLogMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

SessionDep = Annotated[Session, Depends(get_db)]

app = FastAPI(lifespan=lifespan)


app.add_middleware(AuditLogMiddleware)
# This listener is good to audit what happens in the database but for auditing the API requests,
# we need to use middleware.
# def audit_listener(mapper, connection, target):
#     with Session(bind=connection) as session:
#         log_entry = AuditLog(
#             table_name=target.__tablename__,
#             record_id=target.id,
#             user_id=1,
#             action="INSERT",
#             new_value=str(target.__dict__),
#         )
#         session.add(log_entry)
#         session.commit()
#
# event.listen(Item, "after_insert", audit_listener)



@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.post("/token")
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token({"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Security(oauth2_scheme)):
    return {"username": get_current_user(token)}

@app.get("/items/{item_id}")
def get_item(item_id: str, session: SessionDep) -> Item:
    result = session.exec(select(Item).where(Item.id == item_id)).first()
    return Item(name=item_id)


@app.get("/items/")
def get_items(session: SessionDep) -> list[Item]:
    result = session.execute(select(Item)).all()
    return result


@app.post("/items/", status_code=201)
def create_item(item: Item, session: SessionDep) -> Item:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/audit_log/")
def get_audit_log(session: Session = Depends(get_db)) -> list[Annotated[AuditLog, {"exclude": True}]] :
    result = session.execute(select(AuditLog)).scalars()
    return result
