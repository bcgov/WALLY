"""
Main application entrypoint that initializes FastAPI and registers the endpoints defined in api/router.py.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response

from starlette_exporter import PrometheusMiddleware, handle_metrics

from api import config
from api.router import api_router
from api.db.session import Session

wally_api = FastAPI(title=config.PROJECT_NAME,
                    openapi_url="/api/v1/openapi.json")


wally_api.add_middleware(PrometheusMiddleware, app_name="wally")
wally_api.add_route("/metrics", handle_metrics)

# CORS
origins = ["*"]

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    wally_api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"]
    ),

wally_api.add_middleware(GZipMiddleware)

wally_api.include_router(api_router, prefix=config.API_V1_STR)


@wally_api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


@wally_api.get("/health")
def health_check():
    return Response(status_code=200, content=b"")
