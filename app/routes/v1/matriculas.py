from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.domain.schemas.matricula import (
    MatriculaCreate,
    MatriculaResponse
)
from app.services import matricula_service


router = APIRouter(
    prefix="/matriculas",
    tags=["Matrículas"]
)


@router.post(
    "",
    response_model=MatriculaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_matricula(
    dados: MatriculaCreate,
    db: Session = Depends(get_db)
):
    try:
        return matricula_service.criar_matricula(db, dados)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )


@router.get(
    "",
    response_model=list[MatriculaResponse]
)
def listar_matriculas(db: Session = Depends(get_db)):
    return matricula_service.listar_matriculas(db)


@router.get(
    "/{matricula_id}",
    response_model=MatriculaResponse
)
def buscar_matricula(
    matricula_id: int,
    db: Session = Depends(get_db)
):
    matricula = matricula_service.buscar_matricula(
        db,
        matricula_id
    )

    if matricula is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula não encontrada"
        )

    return matricula


@router.patch(
    "/{matricula_id}/cancelar",
    response_model=MatriculaResponse
)
def cancelar_matricula(
    matricula_id: int,
    db: Session = Depends(get_db)
):
    try:
        matricula = matricula_service.cancelar_matricula(
            db,
            matricula_id
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )

    if matricula is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula não encontrada"
        )

    return matricula