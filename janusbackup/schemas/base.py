from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field

__all__ = ["BaseModel", "BaseModelORM", "BasePaginator", "Field"]


class BaseModel(PydanticBaseModel):
    class Config:
        json_encoders = {}


class BaseModelORM(BaseModel):
    class Config(BaseModel.Config):
        orm_mode = True


class BasePaginator(BaseModel):
    result: list = Field(default=[])
    total: int = Field(default=0)
