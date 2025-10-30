from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handler import users, customers, cars, customer_car, workshops

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
app.include_router(users.router, prefix=api_route, tags=["users"])
app.include_router(customers.router, prefix=api_route, tags=["customers"])
app.include_router(cars.router, prefix=api_route, tags=["cars"])
app.include_router(customer_car.router, prefix=api_route, tags=["customer_car"])
app.include_router(workshops.router, prefix=api_route, tags=["workshops"])

@app.get("/")
async def root():
    return {"message": "Welcome to Taller API"}