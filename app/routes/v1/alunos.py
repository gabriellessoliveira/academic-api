from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.domain.schemas.aluno import AlunoCreate, AlunoResponse
from app.services import aluno_service


router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)


@router.post(
    "",
    response_model=AlunoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_aluno(
    dados: AlunoCreate,
    db: Session = Depends(get_db)
):
    try:
        return aluno_service.criar_aluno(db, dados)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )


@router.get(
    "",
    response_model=list[AlunoResponse]
)
def listar_alunos(db: Session = Depends(get_db)):
    return aluno_service.listar_alunos(db)


@router.get(
    "/{aluno_id}",
    response_model=AlunoResponse
)
def buscar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    aluno = aluno_service.buscar_aluno(db, aluno_id)

    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    return aluno


@router.put(
    "/{aluno_id}",
    response_model=AlunoResponse
)
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoCreate,
    db: Session = Depends(get_db)
):
    try:
        aluno = aluno_service.atualizar_aluno(
            db,
            aluno_id,
            dados
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )

    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    return aluno


@router.delete(
    "/{aluno_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    excluido = aluno_service.excluir_aluno(db, aluno_id)

    if not excluido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)