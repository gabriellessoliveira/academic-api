from pydantic import BaseModel, ConfigDict, Field


class DisciplinaBase(BaseModel):
    nome: str = Field(min_length=3, max_length=150)
    codigo: str = Field(min_length=2, max_length=30)
    carga_horaria: int = Field(gt=0)
    professor_id: int = Field(gt=0)


class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaResponse(DisciplinaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)