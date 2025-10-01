from fastapi import FastAPI
from getShifts import router as shifts_router
from login import router as login_router
from updataShifts import router as updata_shifts_router


app = FastAPI(
    title="シフト管理API",
    description="シフトの閲覧・更新を行うためのAPIです。",
    version="1.0.0",
)


app.include_router(login_router)
app.include_router(shifts_router)
app.include_router(updata_shifts_router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Shift Management API"}