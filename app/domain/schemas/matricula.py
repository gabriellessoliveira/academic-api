from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MatriculaCreate(BaseModel):
    aluno_id: int = Field(gt=0)
    turma_id: int = Field(gt=0)


class MatriculaResponse(BaseModel):
    id: int
    aluno_id: int
    turma_id: int
    data: date
    status: Literal["ativa", "cancelada", "concluida"]

    model_config = ConfigDict(from_attributes=True)