from fastapi import APIRouter

from app.routes.v1.alunos import router as alunos_router
from app.routes.v1.disciplinas import router as disciplinas_router
from app.routes.v1.health import router as health_router
from app.routes.v1.matriculas import router as matriculas_router
from app.routes.v1.notas import router as notas_router
from app.routes.v1.relatorios import router as relatorios_router
from app.routes.v1.turmas import router as turmas_router


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(alunos_router)
api_router.include_router(disciplinas_router)
api_router.include_router(turmas_router)
api_router.include_router(matriculas_router)
api_router.include_router(notas_router)
api_router.include_router(relatorios_router)