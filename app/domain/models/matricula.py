from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Matricula(Base):
    __tablename__ = "matriculas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    aluno_id: Mapped[int] = mapped_column(
        ForeignKey("alunos.id"),
        nullable=False
    )

    turma_id: Mapped[int] = mapped_column(
        ForeignKey("turmas.id"),
        nullable=False
    )

    data: Mapped[date] = mapped_column(
        Date,
        default=date.today,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ativa",
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('ativa', 'cancelada', 'concluida')",
            name="ck_matricula_status"
        ),
        UniqueConstraint(
            "aluno_id",
            "turma_id",
            name="uq_aluno_turma"
        ),
    )