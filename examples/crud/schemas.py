from pydantic import BaseModel


class Product(BaseModel):
    id: int | None = None
    name: str
    description: str
    code: str

