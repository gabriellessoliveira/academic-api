from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.models.aluno import Aluno
from app.domain.models.matricula import Matricula
from app.domain.models.turma import Turma
from app.domain.schemas.matricula import MatriculaCreate


def listar_matriculas(db: Session):
    consulta = select(Matricula).order_by(Matricula.id)

    return db.scalars(consulta).all()


def buscar_matricula(db: Session, matricula_id: int):
    return db.get(Matricula, matricula_id)


def criar_matricula(
    db: Session,
    dados: MatriculaCreate
):
    aluno = db.get(Aluno, dados.aluno_id)

    if aluno is None:
        raise ValueError("Aluno não encontrado")

    turma = db.get(Turma, dados.turma_id)

    if turma is None:
        raise ValueError("Turma não encontrada")

    matricula_existente = db.scalar(
        select(Matricula).where(
            Matricula.aluno_id == dados.aluno_id,
            Matricula.turma_id == dados.turma_id
        )
    )

    if matricula_existente is not None:
        raise ValueError(
            "Aluno já possui matrícula nessa turma"
        )

    quantidade_matriculados = db.scalar(
        select(func.count(Matricula.id)).where(
            Matricula.turma_id == dados.turma_id,
            Matricula.status == "ativa"
        )
    )

    if quantidade_matriculados >= turma.vagas:
        raise ValueError("Turma sem vagas disponíveis")

    matricula = Matricula(
        aluno_id=dados.aluno_id,
        turma_id=dados.turma_id,
        status="ativa"
    )

    db.add(matricula)
    db.commit()
    db.refresh(matricula)

    return matricula


def cancelar_matricula(
    db: Session,
    matricula_id: int
):
    matricula = buscar_matricula(db, matricula_id)

    if matricula is None:
        return None

    if matricula.status == "cancelada":
        raise ValueError("Matrícula já está cancelada")

    if matricula.status == "concluida":
        raise ValueError(
            "Matrícula concluída não pode ser cancelada"
        )

    matricula.status = "cancelada"

    db.commit()
    db.refresh(matricula)

    return matricula