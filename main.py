from fastapi import FastAPI
from app.core.db.config import init_db
from app.features.users.api.routes import router as users_router
from app.features.unidades.api.routes import router as unidades_router
from app.features.rutas.api.routes import router as rutas_router

app = FastAPI(title="Backend Control Transportistas", version="1.0.0")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(users_router)
app.include_router(unidades_router)
app.include_router(rutas_router)


@app.get("/")
def root():
    return {"message": "Welcome to Backend Control Transportistas API"}
