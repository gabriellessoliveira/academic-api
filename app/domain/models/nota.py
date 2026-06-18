from sqlalchemy import CheckConstraint, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Nota(Base):
    __tablename__ = "notas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    matricula_id: Mapped[int] = mapped_column(
        ForeignKey("matriculas.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    valor: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('N1', 'N2', 'N3', 'Final')",
            name="ck_nota_tipo"
        ),
        CheckConstraint(
            "valor >= 0 AND valor <= 10",
            name="ck_nota_valor"
        ),
        UniqueConstraint(
            "matricula_id",
            "tipo",
            name="uq_nota_matricula_tipo"
        ),
    )