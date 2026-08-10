from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.base_datos import inicializar
from routers import usuario, ingrediente, receta, postre, venta

app = FastAPI(
    title="LUKELIAH",
    version="1.0",
    description="API REST del sistema LUKELIAH"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()

app.include_router(usuario.router)
app.include_router(ingrediente.router)
app.include_router(receta.router)
app.include_router(postre.router)
app.include_router(venta.router)

@app.get("/")
def inicio():
    return {
        "mensaje": "API LUKELIAH funcionando",
        "version": "1.0",
        "docs": "/docs"
    }