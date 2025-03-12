from fastapi import FastAPI
from app.routers import items

app = FastAPI(title="FastAPI SonarQube Example")

# Include routers
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}