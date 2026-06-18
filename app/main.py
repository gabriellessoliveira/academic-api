from fastapi import FastAPI

from app.database.base import Base
from app.database.session import engine
from app.domain import models
from app.routes.v1.router import api_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Academic API",
    description="API REST para gerenciamento acadêmico",
    version="1.0.0"
)

app.include_router(api_router, prefix="/v1")


@app.get("/")
def raiz():
    return {
        "mensagem": "Academic API em execução"
    }