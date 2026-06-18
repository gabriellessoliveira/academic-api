from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.domain.schemas.turma import TurmaCreate, TurmaResponse
from app.services import turma_service


router = APIRouter(
    prefix="/turmas",
    tags=["Turmas"]
)


@router.post(
    "",
    response_model=TurmaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_turma(
    dados: TurmaCreate,
    db: Session = Depends(get_db)
):
    try:
        return turma_service.criar_turma(db, dados)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )


@router.get(
    "",
    response_model=list[TurmaResponse]
)
def listar_turmas(db: Session = Depends(get_db)):
    return turma_service.listar_turmas(db)


@router.get(
    "/{turma_id}",
    response_model=TurmaResponse
)
def buscar_turma(
    turma_id: int,
    db: Session = Depends(get_db)
):
    turma = turma_service.buscar_turma(db, turma_id)

    if turma is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )

    return turma


@router.put(
    "/{turma_id}",
    response_model=TurmaResponse
)
def atualizar_turma(
    turma_id: int,
    dados: TurmaCreate,
    db: Session = Depends(get_db)
):
    try:
        turma = turma_service.atualizar_turma(
            db,
            turma_id,
            dados
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )

    if turma is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )

    return turma


@router.delete(
    "/{turma_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_turma(
    turma_id: int,
    db: Session = Depends(get_db)
):
    excluida = turma_service.excluir_turma(db, turma_id)

    if not excluida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)