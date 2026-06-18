from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.domain.schemas.disciplina import (
    DisciplinaCreate,
    DisciplinaResponse
)
from app.services import disciplina_service


router = APIRouter(
    prefix="/disciplinas",
    tags=["Disciplinas"]
)


@router.post(
    "",
    response_model=DisciplinaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_disciplina(
    dados: DisciplinaCreate,
    db: Session = Depends(get_db)
):
    try:
        return disciplina_service.criar_disciplina(db, dados)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )


@router.get(
    "",
    response_model=list[DisciplinaResponse]
)
def listar_disciplinas(db: Session = Depends(get_db)):
    return disciplina_service.listar_disciplinas(db)


@router.get(
    "/{disciplina_id}",
    response_model=DisciplinaResponse
)
def buscar_disciplina(
    disciplina_id: int,
    db: Session = Depends(get_db)
):
    disciplina = disciplina_service.buscar_disciplina(
        db,
        disciplina_id
    )

    if disciplina is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )

    return disciplina


@router.put(
    "/{disciplina_id}",
    response_model=DisciplinaResponse
)
def atualizar_disciplina(
    disciplina_id: int,
    dados: DisciplinaCreate,
    db: Session = Depends(get_db)
):
    try:
        disciplina = disciplina_service.atualizar_disciplina(
            db,
            disciplina_id,
            dados
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )

    if disciplina is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )

    return disciplina


@router.delete(
    "/{disciplina_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_disciplina(
    disciplina_id: int,
    db: Session = Depends(get_db)
):
    excluida = disciplina_service.excluir_disciplina(
        db,
        disciplina_id
    )

    if not excluida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)