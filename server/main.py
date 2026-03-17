from fastapi import BackgroundTasks, FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from config.database.index import initalize_database
from utils.errors.index import AppException
from utils.response.index import ResponseModel
from utils.models.model_loader import load_model
from routes.index import router
import schemas
from fastapi.staticfiles import StaticFiles


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
async def test(background_task : BackgroundTasks ):
    print(background_task)
    return 1

app.include_router(router, prefix="/api")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
