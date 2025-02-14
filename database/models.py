from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

from database.database_creation import engine


# I'm using SQLModel to define the models and schemas together, so I don't have code duplication.
# But I think this could be a problem if the representation of the model in the database is different from the
# representation of the model in the API.


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, exclude=True)
    table_name: str
    record_id: int
    user_id: int
    action: str # insert, update, delete
    timestamp: datetime = Field(default=datetime.now())
    old_value: Optional[str] = None
    new_value: Optional[str] = None


def create_db_and_tables():
    from sqlmodel import inspect
    print("Before table creation:", inspect(engine).get_table_names())
    SQLModel.metadata.create_all(bind=engine)
    print("After table creation:", inspect(engine).get_table_names())
