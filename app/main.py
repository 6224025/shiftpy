from fastapi import FastAPI
from .config import settings 
from .routers import login,  getShifts, updataShifts


app = FastAPI(
    title=settings.APP_TITLE,
    description="シフトの閲覧・更新を行うためのAPIです。",
    version="1.0.0",
)


app.include_router(login.router)
app.include_router(getShifts.router)
app.include_router(updataShifts.router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Shift Management API"}