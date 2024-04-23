from pydantic import BaseModel


class ProductCreateSchema(BaseModel):
    name: str
    description: str


class ProductReadSchema(BaseModel):
    id: int | None = None
    name: str
    description: str
    code: str


class ProductUpdateSchema(BaseModel):
    name: str = None
    description: str = None
