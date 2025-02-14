from pydantic import BaseModel


class ItemPostSchema(BaseModel):
    name: str
