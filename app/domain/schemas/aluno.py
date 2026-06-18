from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AlunoBase(BaseModel):
    nome: str = Field(min_length=3, max_length=150)
    email: EmailStr
    matricula: str = Field(min_length=3, max_length=30)
    periodo: int = Field(ge=1, le=20)


class AlunoCreate(AlunoBase):
    pass


class AlunoResponse(AlunoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)