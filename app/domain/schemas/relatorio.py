from pydantic import BaseModel


class NotaBoletim(BaseModel):
    tipo: str
    valor: float


class DisciplinaBoletim(BaseModel):
    disciplina_id: int
    disciplina: str
    codigo: str
    notas: list[NotaBoletim]
    media: float | None


class BoletimAluno(BaseModel):
    aluno_id: int
    aluno: str
    matricula: str
    disciplinas: list[DisciplinaBoletim]