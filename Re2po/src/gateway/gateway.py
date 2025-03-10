from fastapi import FastAPI, UploadFile, BackgroundTasks
import uvicorn
from ..services import service as model_service

app = FastAPI()


@app.post("/minio/upload", summary="upload")
async def upload(file: UploadFile):
    return await model_service.upload(file)

@app.post("/minio/upload_", summary="upload_")
async def upload(file: UploadFile):
    return await model_service.upload_(file)

@app.post("/minio/download", summary="download")
async def download(model_name: str, background_task: BackgroundTasks):
    return await model_service.download(model_name, background_task)

@app.post("/minio/download_", summary="download_")
async def download(model_name: str, background_task: BackgroundTasks):
    return await model_service.download_(model_name, background_task)

@app.post("/minio/delete_all", summary=" delete_all")
async def delete_all():
    return await model_service.delete_all()

@app.post("/minio/delete_all_", summary=" delete_all_")
async def delete_all():
    return await model_service.delete_all_2()

@app.post("/minio/delete", summary="delete")
async def delete_by_model_name(model_name: str):
    return await model_service.delete_by_model_name(model_name)

if __name__ == "__main__":
    uvicorn.run(app='gateway:app', host='0.0.0.0', port=8000, reload=True)
