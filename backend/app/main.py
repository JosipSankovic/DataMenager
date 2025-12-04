from app.routers import ProjectsRouter, ImagesRouter,LabelsRouter,VersionsRouter,DatasetsRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Create the database tables

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
app.include_router(LabelsRouter)
app.include_router(VersionsRouter)
app.include_router(DatasetsRouter)


