from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.domain.models.aluno import Aluno
from app.domain.schemas.aluno import AlunoCreate


def listar_alunos(db: Session):
    consulta = select(Aluno).order_by(Aluno.id)

    return db.scalars(consulta).all()


def buscar_aluno(db: Session, aluno_id: int):
    return db.get(Aluno, aluno_id)


def verificar_duplicidade(
    db: Session,
    email: str,
    matricula: str,
    aluno_id: int | None = None
):
    consulta = select(Aluno).where(
        or_(
            Aluno.email == email,
            Aluno.matricula == matricula
        )
    )

    if aluno_id is not None:
        consulta = consulta.where(Aluno.id != aluno_id)

    return db.scalar(consulta) is not None


def criar_aluno(db: Session, dados: AlunoCreate):
    if verificar_duplicidade(
        db,
        dados.email,
        dados.matricula
    ):
        raise ValueError("E-mail ou matrícula já cadastrados")

    aluno = Aluno(
        nome=dados.nome,
        email=dados.email,
        matricula=dados.matricula,
        periodo=dados.periodo
    )

    db.add(aluno)
    db.commit()
    db.refresh(aluno)

    return aluno


def atualizar_aluno(
    db: Session,
    aluno_id: int,
    dados: AlunoCreate
):
    aluno = buscar_aluno(db, aluno_id)

    if aluno is None:
        return None

    if verificar_duplicidade(
        db,
        dados.email,
        dados.matricula,
        aluno_id
    ):
        raise ValueError("E-mail ou matrícula já cadastrados")

    aluno.nome = dados.nome
    aluno.email = dados.email
    aluno.matricula = dados.matricula
    aluno.periodo = dados.periodo

    db.commit()
    db.refresh(aluno)

    return aluno


def excluir_aluno(db: Session, aluno_id: int):
    aluno = buscar_aluno(db, aluno_id)

    if aluno is None:
        return False

    db.delete(aluno)
    db.commit()

    return True