from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class NotaCreate(BaseModel):
    matricula_id: int = Field(gt=0)
    tipo: Literal["N1", "N2", "N3", "Final"]
    valor: float = Field(ge=0, le=10)


class NotaUpdate(BaseModel):
    valor: float = Field(ge=0, le=10)


class NotaResponse(BaseModel):
    id: int
    matricula_id: int
    tipo: Literal["N1", "N2", "N3", "Final"]
    valor: float

    model_config = ConfigDict(from_attributes=True)