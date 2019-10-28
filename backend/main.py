"""
Main application entrypoint that initializes FastAPI and registers the endpoints defined in app/router.py.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette_exporter import PrometheusMiddleware, handle_metrics
from app import config
from app.router import api_router
from app.db.session import Session

app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")


app.add_middleware(PrometheusMiddleware)

# CORS
origins = ["*"]

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.add_middleware(GZipMiddleware)

app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response

# expose metrics for Prometheus scraping.
app.add_route("/metrics", handle_metrics)


@app.get("/health")
def health_check():
    return Response(status_code=200, content=b"")
