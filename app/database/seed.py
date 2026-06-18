from sqlalchemy import select
from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.domain.models.aluno import Aluno
from app.domain.models.disciplina import Disciplina
from app.domain.models.matricula import Matricula
from app.domain.models.nota import Nota
from app.domain.models.professor import Professor
from app.domain.models.turma import Turma


professores = [
    {
        "nome": "Clayton Compiladores",
        "email": "clayton.compiladores@faculdade.com",
        "especialidade": "Compiladores"
    },
    {
        "nome": "Fernando Framework",
        "email": "fernando.framework@faculdade.com",
        "especialidade": "Desenvolvimento de Framework"
    },
    {
        "nome": "Roger Software",
        "email": "roger.software@faculdade.com",
        "especialidade": "Arquitetura de Software"
    }
]


alunos = [
    {
        "nome": "Bruna Biancardi",
        "email": "bruna.biancardi@example.com",
        "matricula": "2026001",
        "periodo": 2
    },
    {
        "nome": "Simone Mendes",
        "email": "simone.mendes@example.com",
        "matricula": "2026002",
        "periodo": 4
    },
    {
        "nome": "Cacau Casonato",
        "email": "cacau.casonato@example.com",
        "matricula": "2026003",
        "periodo": 3
    },
    {
        "nome": "Luan Santana",
        "email": "luan.santana@example.com",
        "matricula": "2026004",
        "periodo": 5
    },
    {
        "nome": "Alisson Dilaurentis",
        "email": "alisson.dilaurentis@example.com",
        "matricula": "2026005",
        "periodo": 6
    }
]


disciplinas = [
    {
        "nome": "Compiladores",
        "codigo": "COMP01",
        "carga_horaria": 100,
        "professor_email": "clayton.compiladores@faculdade.com"
    },
    {
        "nome": "Desenvolvimento de Framework",
        "codigo": "FRAME01",
        "carga_horaria": 80,
        "professor_email": "fernando.framework@faculdade.com"
    },
    {
        "nome": "Arquitetura de Software",
        "codigo": "ARQ01",
        "carga_horaria": 80,
        "professor_email": "roger.software@faculdade.com"
    },
    {
        "nome": "Laboratório de Algoritmos",
        "codigo": "LABALG01",
        "carga_horaria": 60,
        "professor_email": "clayton.compiladores@faculdade.com"
    }
]


turmas = [
    {
        "codigo_disciplina": "COMP01",
        "semestre": 2,
        "ano": 2026,
        "vagas": 40
    },
    {
        "codigo_disciplina": "FRAME01",
        "semestre": 2,
        "ano": 2026,
        "vagas": 40
    },
    {
        "codigo_disciplina": "ARQ01",
        "semestre": 2,
        "ano": 2026,
        "vagas": 40
    },
    {
        "codigo_disciplina": "LABALG01",
        "semestre": 2,
        "ano": 2026,
        "vagas": 40
    }
]


matriculas_e_notas = {
    "2026001": {
        "COMP01": {
            "N1": 8.0,
            "N2": 7.5
        },
        "ARQ01": {
            "N1": 9.0,
            "N2": 8.5
        }
    },
    "2026002": {
        "FRAME01": {
            "N1": 7.0,
            "N2": 8.0
        },
        "LABALG01": {
            "N1": 8.5,
            "N2": 9.0
        }
    },
    "2026003": {
        "COMP01": {
            "N1": 6.5,
            "N2": 7.5
        },
        "FRAME01": {
            "N1": 8.0,
            "N2": 8.5
        }
    },
    "2026004": {
        "ARQ01": {
            "N1": 7.5,
            "N2": 8.0
        },
        "LABALG01": {
            "N1": 9.0,
            "N2": 9.5
        }
    },
    "2026005": {
        "COMP01": {
            "N1": 8.5,
            "N2": 9.0
        },
        "ARQ01": {
            "N1": 7.0,
            "N2": 8.0
        }
    }
}


def buscar_ou_criar_professor(db, dados):
    professor = db.scalar(
        select(Professor).where(
            Professor.email == dados["email"]
        )
    )

    if professor is None:
        professor = Professor(**dados)
        db.add(professor)
        db.flush()

    return professor


def buscar_ou_criar_aluno(db, dados):
    aluno = db.scalar(
        select(Aluno).where(
            Aluno.matricula == dados["matricula"]
        )
    )

    if aluno is None:
        aluno = Aluno(**dados)
        db.add(aluno)
        db.flush()

    return aluno


def buscar_ou_criar_disciplina(db, dados, professor):
    disciplina = db.scalar(
        select(Disciplina).where(
            Disciplina.codigo == dados["codigo"]
        )
    )

    if disciplina is None:
        disciplina = Disciplina(
            nome=dados["nome"],
            codigo=dados["codigo"],
            carga_horaria=dados["carga_horaria"],
            professor_id=professor.id
        )

        db.add(disciplina)
        db.flush()

    return disciplina


def buscar_ou_criar_turma(db, dados, disciplina):
    turma = db.scalar(
        select(Turma).where(
            Turma.disciplina_id == disciplina.id,
            Turma.semestre == dados["semestre"],
            Turma.ano == dados["ano"]
        )
    )

    if turma is None:
        turma = Turma(
            disciplina_id=disciplina.id,
            semestre=dados["semestre"],
            ano=dados["ano"],
            vagas=dados["vagas"]
        )

        db.add(turma)
        db.flush()

    return turma


def buscar_ou_criar_matricula(db, aluno, turma):
    matricula = db.scalar(
        select(Matricula).where(
            Matricula.aluno_id == aluno.id,
            Matricula.turma_id == turma.id
        )
    )

    if matricula is None:
        matricula = Matricula(
            aluno_id=aluno.id,
            turma_id=turma.id,
            status="ativa"
        )

        db.add(matricula)
        db.flush()

    return matricula


def buscar_ou_criar_nota(
    db,
    matricula,
    tipo,
    valor
):
    nota = db.scalar(
        select(Nota).where(
            Nota.matricula_id == matricula.id,
            Nota.tipo == tipo
        )
    )

    if nota is None:
        nota = Nota(
            matricula_id=matricula.id,
            tipo=tipo,
            valor=valor
        )

        db.add(nota)
    else:
        nota.valor = valor


def executar_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        professores_banco = {}

        for dados in professores:
            professor = buscar_ou_criar_professor(
                db,
                dados
            )

            professores_banco[dados["email"]] = professor

        alunos_banco = {}

        for dados in alunos:
            aluno = buscar_ou_criar_aluno(
                db,
                dados
            )

            alunos_banco[dados["matricula"]] = aluno

        disciplinas_banco = {}

        for dados in disciplinas:
            professor = professores_banco[
                dados["professor_email"]
            ]

            disciplina = buscar_ou_criar_disciplina(
                db,
                dados,
                professor
            )

            disciplinas_banco[dados["codigo"]] = disciplina

        turmas_banco = {}

        for dados in turmas:
            disciplina = disciplinas_banco[
                dados["codigo_disciplina"]
            ]

            turma = buscar_ou_criar_turma(
                db,
                dados,
                disciplina
            )

            turmas_banco[
                dados["codigo_disciplina"]
            ] = turma

        for numero_matricula, disciplinas_aluno in (
            matriculas_e_notas.items()
        ):
            aluno = alunos_banco[numero_matricula]

            for codigo, notas in disciplinas_aluno.items():
                turma = turmas_banco[codigo]

                matricula = buscar_ou_criar_matricula(
                    db,
                    aluno,
                    turma
                )

                for tipo, valor in notas.items():
                    buscar_ou_criar_nota(
                        db,
                        matricula,
                        tipo,
                        valor
                    )

        db.commit()

        print("Seed executado com sucesso.")
        print("5 alunos cadastrados.")
        print("3 professores cadastrados.")
        print("4 disciplinas cadastradas.")
        print("Matrículas e notas cadastradas.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    executar_seed()

