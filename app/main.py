from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app import config
from app.middlewares.execution_time_logging import ExecutionTimeLoggingMiddleware
from app.routers import users

app = FastAPI(openapi_url="/openapi.json" if config.enable_docs else None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if config.profile_endpoints:
    app.add_middleware(ExecutionTimeLoggingMiddleware)


app.include_router(users.router, prefix="/users")


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "Ok"}


handler = Mangum(app)
