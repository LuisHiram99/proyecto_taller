from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handler.users import users
from handler import customers, cars, customer_car, workshops
from handler.current_user import current_user
from auth import auth
from typing import Annotated


description = """
API created for the Taller project.
"""

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations related to user authentication and token management.",
    },
    {
        "name": "users",
        "description": "Operations related to user management. Only accessible by admin users.",
    },
    {
        "name": "current_user",
        "description": "Operations related to the currently authenticated user.",
    },
    {
        "name": "customers",
        "description": "Operations related to customer management. Only accessible by admin users.",
    },
    {
        "name": "cars",
        "description": "Operations related to car management. Only accessible by admin users.",
    },
    {
        "name": "customer_car",
        "description": "Operations related to managing the association between customers and their cars. Only accessible by admin users.",
    },
    {
        "name": "workshops",
        "description": "Operations related to workshop management. Only accessible by admin users.",
    },
]

app = FastAPI(
    title="Taller API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata
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
app.include_router(auth.router, prefix=api_route, tags=["auth"])
app.include_router(users.router, prefix=api_route, tags=["users"])
app.include_router(current_user.router, prefix=api_route, tags=["current_user"])
app.include_router(customers.router, prefix=api_route, tags=["customers"])
app.include_router(cars.router, prefix=api_route, tags=["cars"])
app.include_router(customer_car.router, prefix=api_route, tags=["customer_car"])
app.include_router(workshops.router, prefix=api_route, tags=["workshops"])

@app.get("/")
async def root():
    return {"message": "Welcome to Taller API"}