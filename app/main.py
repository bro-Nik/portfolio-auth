from fastapi import FastAPI

from app.api.user import user_router
from app.api.admin import admin_router


app = FastAPI(title="Auth Service")

app.include_router(user_router)
app.include_router(admin_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
