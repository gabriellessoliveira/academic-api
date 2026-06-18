from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.disciplina import Disciplina
from app.domain.models.professor import Professor
from app.domain.schemas.disciplina import DisciplinaCreate


def listar_disciplinas(db: Session):
    consulta = select(Disciplina).order_by(Disciplina.id)

    return db.scalars(consulta).all()


def buscar_disciplina(db: Session, disciplina_id: int):
    return db.get(Disciplina, disciplina_id)


def verificar_codigo(
    db: Session,
    codigo: str,
    disciplina_id: int | None = None
):
    consulta = select(Disciplina).where(
        Disciplina.codigo == codigo
    )

    if disciplina_id is not None:
        consulta = consulta.where(
            Disciplina.id != disciplina_id
        )

    return db.scalar(consulta) is not None


def verificar_professor(db: Session, professor_id: int):
    return db.get(Professor, professor_id) is not None


def criar_disciplina(
    db: Session,
    dados: DisciplinaCreate
):
    if verificar_codigo(db, dados.codigo):
        raise ValueError("Código de disciplina já cadastrado")

    if not verificar_professor(db, dados.professor_id):
        raise ValueError("Professor não encontrado")

    disciplina = Disciplina(
        nome=dados.nome,
        codigo=dados.codigo,
        carga_horaria=dados.carga_horaria,
        professor_id=dados.professor_id
    )

    db.add(disciplina)
    db.commit()
    db.refresh(disciplina)

    return disciplina


def atualizar_disciplina(
    db: Session,
    disciplina_id: int,
    dados: DisciplinaCreate
):
    disciplina = buscar_disciplina(db, disciplina_id)

    if disciplina is None:
        return None

    if verificar_codigo(
        db,
        dados.codigo,
        disciplina_id
    ):
        raise ValueError("Código de disciplina já cadastrado")

    if not verificar_professor(db, dados.professor_id):
        raise ValueError("Professor não encontrado")

    disciplina.nome = dados.nome
    disciplina.codigo = dados.codigo
    disciplina.carga_horaria = dados.carga_horaria
    disciplina.professor_id = dados.professor_id

    db.commit()
    db.refresh(disciplina)

    return disciplina


def excluir_disciplina(
    db: Session,
    disciplina_id: int
):
    disciplina = buscar_disciplina(db, disciplina_id)

    if disciplina is None:
        return False

    db.delete(disciplina)
    db.commit()

    return True