from pydantic import BaseModel, ConfigDict, Field


class TurmaBase(BaseModel):
    disciplina_id: int = Field(gt=0)
    semestre: int = Field(ge=1, le=2)
    ano: int = Field(ge=2000)
    vagas: int = Field(gt=0)


class TurmaCreate(TurmaBase):
    pass


class TurmaResponse(TurmaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)