import uvicorn
from fastapi import FastAPI

from app.router import router as router_dwnl
from app.document_router import router as document_router
# from router import router as router_dwnl


app = FastAPI(
    title="Document Processor API",
    description="This service processes documents and returns text fragments with embeddings",
    version="0.0.1",
    redoc_url=None
)

app.include_router(router_dwnl)
app.include_router(document_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
