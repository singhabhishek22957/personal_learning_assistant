
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import client , create_indexes
from fastapi.openapi.utils import get_openapi
from app.core.logging_config import setup_logging
from app.middleware.logging import LoggingMiddleware


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("App is Starting")
    await client.admin.command("ping")
    await create_indexes()


    #  set up logging info 
    setup_logging()

    yield

    await client.close()
    print("App is Shutdown")

app = FastAPI(
    title="Personal Learning AI Assistant",
    version="1.0.0",
    description = "It's help to learning and make schedule for you to execute the any kind of plan in structure way.",
    lifespan = lifespan
)



def custom_api():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {})
    openapi_schema["components"].setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth":{
            "type":"http",
            "scheme":"bearer",
            "bearerFormat":"JWT"
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_api

#  middleware
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#  handling exception 
from app.handler.exceptions import app_exception_handler
from app.core.exceptions import AppException
app.add_exception_handler(AppException, app_exception_handler)

#  routing 

#  auth route

from app.modules.auth.auth_route import router as auth_router
app.include_router(auth_router)

# user route 
from app.modules.user.user_route import router as user_router
app.include_router(user_router)


@app.get('/')
async def root():
    return {
        "message": "Hey, I am the backend of Personal Learning AI Assistant. How can I help you?"
    }

@app.get("/health")
def health():
    return {
        "success":True,
        "message":"the API Health is good"
    }

