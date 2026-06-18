from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)

    codigo: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    carga_horaria: Mapped[int] = mapped_column(nullable=False)

    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professores.id"),
        nullable=False
    )