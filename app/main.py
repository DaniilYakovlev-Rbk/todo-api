from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routers import tasks

def get_application() -> FastAPI:
    application = FastAPI(
        title="Todo API",
        description="REST API для управления списком задач",
    )
    application.include_router(router=tasks.router, tags=["tasks"])
    return application

app = get_application()

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app",
                port=8000, reload=True)