from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import tasks

Base.metadata.create_all(bind=engine)

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