from app.routers import projects
from app.core import engine
from app.models import projects as item_model # Import models so they are registered
from fastapi import FastAPI

# Create the database tables
item_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataMenager API",
    version="0.1.0",
    description="API for managing data projects. You can create and read projects.",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(projects.router)
