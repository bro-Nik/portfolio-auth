from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import routes
from app.db.connection import db
from app.db.init_db import init_db


app = FastAPI(title="Auth Service")
app.include_router(routes.router)


@app.on_event("startup")
async def startup():
    await db.connect()
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
