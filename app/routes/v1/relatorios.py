from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.domain.schemas.relatorio import BoletimAluno
from app.services import relatorio_service


router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)


@router.get(
    "/alunos/{aluno_id}/boletim",
    response_model=BoletimAluno
)
def gerar_boletim(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    boletim = relatorio_service.gerar_boletim(
        db,
        aluno_id
    )

    if boletim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    return boletim