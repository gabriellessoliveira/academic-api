from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.disciplina import Disciplina
from app.domain.models.turma import Turma
from app.domain.schemas.turma import TurmaCreate


def listar_turmas(db: Session):
    consulta = select(Turma).order_by(Turma.id)

    return db.scalars(consulta).all()


def buscar_turma(db: Session, turma_id: int):
    return db.get(Turma, turma_id)


def verificar_disciplina(db: Session, disciplina_id: int):
    return db.get(Disciplina, disciplina_id) is not None


def criar_turma(db: Session, dados: TurmaCreate):
    if not verificar_disciplina(db, dados.disciplina_id):
        raise ValueError("Disciplina não encontrada")

    turma = Turma(
        disciplina_id=dados.disciplina_id,
        semestre=dados.semestre,
        ano=dados.ano,
        vagas=dados.vagas
    )

    db.add(turma)
    db.commit()
    db.refresh(turma)

    return turma


def atualizar_turma(
    db: Session,
    turma_id: int,
    dados: TurmaCreate
):
    turma = buscar_turma(db, turma_id)

    if turma is None:
        return None

    if not verificar_disciplina(db, dados.disciplina_id):
        raise ValueError("Disciplina não encontrada")

    turma.disciplina_id = dados.disciplina_id
    turma.semestre = dados.semestre
    turma.ano = dados.ano
    turma.vagas = dados.vagas

    db.commit()
    db.refresh(turma)

    return turma


def excluir_turma(db: Session, turma_id: int):
    turma = buscar_turma(db, turma_id)

    if turma is None:
        return False

    db.delete(turma)
    db.commit()

    return True