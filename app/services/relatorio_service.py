from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.aluno import Aluno
from app.domain.models.disciplina import Disciplina
from app.domain.models.matricula import Matricula
from app.domain.models.nota import Nota
from app.domain.models.turma import Turma


def gerar_boletim(db: Session, aluno_id: int):
    aluno = db.get(Aluno, aluno_id)

    if aluno is None:
        return None

    consulta = (
        select(Matricula, Turma, Disciplina)
        .join(Turma, Matricula.turma_id == Turma.id)
        .join(
            Disciplina,
            Turma.disciplina_id == Disciplina.id
        )
        .where(
            Matricula.aluno_id == aluno_id,
            Matricula.status != "cancelada"
        )
        .order_by(Disciplina.nome)
    )

    registros = db.execute(consulta).all()

    disciplinas = []

    for matricula, turma, disciplina in registros:
        consulta_notas = (
            select(Nota)
            .where(Nota.matricula_id == matricula.id)
            .order_by(Nota.id)
        )

        notas_banco = db.scalars(consulta_notas).all()

        notas = [
            {
                "tipo": nota.tipo,
                "valor": nota.valor
            }
            for nota in notas_banco
        ]

        if notas_banco:
            soma = sum(nota.valor for nota in notas_banco)
            media = round(soma / len(notas_banco), 2)
        else:
            media = None

        disciplinas.append(
            {
                "disciplina_id": disciplina.id,
                "disciplina": disciplina.nome,
                "codigo": disciplina.codigo,
                "notas": notas,
                "media": media
            }
        )

    return {
        "aluno_id": aluno.id,
        "aluno": aluno.nome,
        "matricula": aluno.matricula,
        "disciplinas": disciplinas
    }