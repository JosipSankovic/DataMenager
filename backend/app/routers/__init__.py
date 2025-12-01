from app.routers.projects import router as ProjectsRouter
from app.routers.images import router as ImagesRouter
from app.routers.labels import router as LabelsRouter
from app.routers.versions import router as VersionsRouter

__all__ = ["ProjectsRouter","ImagesRouter","LabelsRouter","VersionsRouter"]