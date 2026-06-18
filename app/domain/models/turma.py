from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Turma(Base):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey("disciplinas.id"),
        nullable=False
    )

    semestre: Mapped[int] = mapped_column(nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)
    vagas: Mapped[int] = mapped_column(nullable=False)