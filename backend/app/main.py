from app.routers import ProjectsRouter, ImagesRouter
from app.core import engine
from app.models import projects as item_model # Import models so they are registered
from app.models import images as images_model
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Create the database tables
item_model.Base.metadata.create_all(bind=engine)
images_model.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="DataMenager API",
    version="0.1.0",
    description="API for managing data projects. You can create and read projects.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(ProjectsRouter)
app.include_router(ImagesRouter)