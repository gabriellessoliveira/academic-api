from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.domain.schemas.nota import (
    NotaCreate,
    NotaResponse,
    NotaUpdate
)
from app.services import nota_service


router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)


@router.post(
    "",
    response_model=NotaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_nota(
    dados: NotaCreate,
    db: Session = Depends(get_db)
):
    try:
        return nota_service.criar_nota(db, dados)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )


@router.get(
    "",
    response_model=list[NotaResponse]
)
def listar_notas(
    matricula_id: int | None = None,
    db: Session = Depends(get_db)
):
    return nota_service.listar_notas(
        db,
        matricula_id
    )


@router.get(
    "/{nota_id}",
    response_model=NotaResponse
)
def buscar_nota(
    nota_id: int,
    db: Session = Depends(get_db)
):
    nota = nota_service.buscar_nota(db, nota_id)

    if nota is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nota não encontrada"
        )

    return nota


@router.patch(
    "/{nota_id}",
    response_model=NotaResponse
)
def atualizar_nota(
    nota_id: int,
    dados: NotaUpdate,
    db: Session = Depends(get_db)
):
    nota = nota_service.atualizar_nota(
        db,
        nota_id,
        dados
    )

    if nota is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nota não encontrada"
        )

    return nota