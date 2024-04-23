from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int | None = None
    name: str
    description: str
    code: str

