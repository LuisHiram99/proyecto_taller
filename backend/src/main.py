from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handler import usuarios, clientes, carros, cliente_carro

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


api_route = "/api/v1"
# Include routers
app.include_router(usuarios.router, prefix=api_route, tags=["usuarios"])
app.include_router(clientes.router, prefix=api_route, tags=["clientes"])
app.include_router(carros.router, prefix=api_route, tags=["carros"])
app.include_router(cliente_carro.router, prefix=api_route, tags=["cliente_carro"])

@app.get("/")
async def root():
    return {"message": "Welcome to Taller API"}