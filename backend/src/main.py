from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handler import usuarios, clientes, carros

app = FastAPI(
    title="Taller API",
    description="API for Taller project",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(usuarios.router, prefix="/api/v1", tags=["usuarios"])
app.include_router(clientes.router, prefix="/api/v1", tags=["clientes"])
app.include_router(carros.router, prefix="/api/v1", tags=["carros"])

@app.get("/")
async def root():
    return {"message": "Welcome to Taller API"}