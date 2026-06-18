from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )
    matricula: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )
    periodo: Mapped[int] = mapped_column(nullable=False)