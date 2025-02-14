from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from sqlmodel import SQLModel, Field

from database.database_creation import engine
from database.db_session import get_db


# I'm using SQLModel to define the models and schemas together, so I don't have code duplication.
# But I think this could be a problem if the representation of the model in the database is different from the
# representation of the model in the API.


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    method: str
    path: str
    timestamp: datetime
    request_body: Optional[str] = None
    response_body: Optional[str] = None
    status_code: int
    user_id: Optional[int] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


def seed_database():
    session = next(get_db())
    user = User(username="test", hashed_password=User.hash_password("test"))
    session.add(user)
    session.commit()

def create_db_and_tables():
    from sqlmodel import inspect
    print("Before table creation:", inspect(engine).get_table_names())
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)

    seed_database()
    print("After table creation:", inspect(engine).get_table_names())
