from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.matricula import Matricula
from app.domain.models.nota import Nota
from app.domain.schemas.nota import NotaCreate, NotaUpdate


def listar_notas(
    db: Session,
    matricula_id: int | None = None
):
    consulta = select(Nota).order_by(Nota.id)

    if matricula_id is not None:
        consulta = consulta.where(
            Nota.matricula_id == matricula_id
        )

    return db.scalars(consulta).all()


def buscar_nota(db: Session, nota_id: int):
    return db.get(Nota, nota_id)


def criar_nota(
    db: Session,
    dados: NotaCreate
):
    matricula = db.get(Matricula, dados.matricula_id)

    if matricula is None:
        raise ValueError("Matrícula não encontrada")

    if matricula.status == "cancelada":
        raise ValueError(
            "Não é possível lançar nota em matrícula cancelada"
        )

    nota_existente = db.scalar(
        select(Nota).where(
            Nota.matricula_id == dados.matricula_id,
            Nota.tipo == dados.tipo
        )
    )

    if nota_existente is not None:
        raise ValueError(
            "Já existe uma nota desse tipo para a matrícula"
        )

    nota = Nota(
        matricula_id=dados.matricula_id,
        tipo=dados.tipo,
        valor=dados.valor
    )

    db.add(nota)
    db.commit()
    db.refresh(nota)

    return nota


def atualizar_nota(
    db: Session,
    nota_id: int,
    dados: NotaUpdate
):
    nota = buscar_nota(db, nota_id)

    if nota is None:
        return None

    nota.valor = dados.valor

    db.commit()
    db.refresh(nota)

    return nota