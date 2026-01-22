from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db.config import init_db
from app.features.users.api.routes import router as users_router
from app.features.unidades.api.routes import router as unidades_router
from app.features.rutas.api.routes import router as rutas_router
from app.features.rendimiento.api.routes import router as rendimiento_router

app = FastAPI(title="Backend Control Transportistas", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(users_router)
app.include_router(unidades_router)
app.include_router(rutas_router)
app.include_router(rendimiento_router)

