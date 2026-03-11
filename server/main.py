from fastapi import Depends, FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from config.database.index import initalize_database
from utils.errors.index import AppException
from utils.response.index import ResponseModel
from utils.models.model_loader import load_model
from routes.index import router
from middlewares.auth_middleware import authenticate

@asynccontextmanager
async def lifespan(app : FastAPI) :
    await initalize_database()
    load_model()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(AppException)
async def custom_exception_handler(request : Request, exception : AppException) :
    content = ResponseModel(success=False, data=None, message=exception.detail)
    return JSONResponse(status_code=exception.status_code, content=content.model_dump())
   
@app.get("/health")
async def health() : 
    return {"message" : "Health of server is top nutch"}

@app.get("/test")
async def test(user_id : int = Depends(authenticate)) : 
    return user_id

app.include_router(router, prefix="/api")
