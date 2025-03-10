from ..dao import storage_dao
from ..dao import data_dao
from ..dao import model_dao
import os
from ..utils.temp_dir import TempDir
from ..utils import minio_utils as utils
import torch
from ..model.entity import ModelInfo, StorageInfo, DataInfo, ModelInfo_2, LocationInfo
from fastapi import FastAPI, UploadFile, BackgroundTasks
from . import model_compose
from starlette.responses import FileResponse
from concurrent.futures import ThreadPoolExecutor, as_completed

import time

def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time} seconds")
        return result
    return wrapper

def remove_file(model_path: str):
    if model_path and os.path.exists(model_path):
        os.remove(model_path)

def get_directory_size(directory_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

async def upload(file: UploadFile):
    file_name = file.filename
    obj_name_prefix = os.path.splitext(file_name)[0]
    minio_size_all = 0
    unre_size_all = 0
    try:
        file_loaded = 0
        minio_count = 0
        disk_spaces = {}
        
        with TempDir() as tmp:
            base_path = tmp.path()
            file_path = os.path.join(base_path, file_name)
            model_path = os.path.join(base_path, "model")
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            model_size_all = os.path.getsize(file_path)
            loaded_model_state = torch.load(file_path, map_location='cpu')
            layer_name_list, layer_hash_list = utils._save_state_dict(state_dict=loaded_model_state, path=model_path)
            utils.common_layer_identification(layer_hash_list)
            files = list(os.scandir(model_path))
            unre_size_all = get_directory_size(model_path)
            file_num = len(files)
            for layer_hash in layer_hash_list:
                print("layer_hash: ", layer_hash)
                file_loaded += 1
                tmp_models = model_dao.get_model_by_layer_hash_all(layer_hash)
                if len(tmp_models) == 0:
                    disks = storage_dao.get_storage_all()
                    for disk in disks:
                        key = disk.minio_id + "_" + disk.minio_location
                        value = disk.free_space
                        disk_spaces[key] = value
                    file_size = os.path.getsize(model_path + "/" + layer_hash + ".pkl")
                    minio_id = utils.get_disk(file_size, disk_spaces)
                    if minio_id == "-1":
                        sql_data = DataInfo(model_name=obj_name_prefix, file_number=file_num,
                                            layer_number=len(layer_hash_list), minio_count=minio_count, complete=0)
                        data_dao.add_data(sql_data)
                        return {"error": "no space", "file_num": file_num, "file_loaded": file_loaded - 1,
                                "layer_hash_len": len(layer_hash_list),
                                "minio_count": minio_count}
                    client = utils.get_client(minio_id)
                    client.fput_object(bucket_name="test", object_name=obj_name_prefix + "/" + layer_hash + ".pkl",
                                       file_path=model_path + "/" + layer_hash + ".pkl")
                    storage = storage_dao.get_storage_by_minio_id(minio_id)
                    storage_dao.update_used_storage(file_size=file_size, storage=storage, minio_id=minio_id)
                    minio_count += 1
                    minio_size_all += file_size

                    db_model = ModelInfo(layer_hash=layer_hash, model_name=obj_name_prefix, minio_id=minio_id,
                                         layer_number=file_loaded, layer_name=layer_name_list[file_loaded - 1],
                                         layer_location=obj_name_prefix,layer_size = file_size)
                    model_dao.add_model(db_model)
                else:
                    for tmp_model in tmp_models:
                        db_model = ModelInfo(layer_hash=tmp_model.layer_hash, model_name=obj_name_prefix,
                                             minio_id=tmp_model.minio_id, layer_number=file_loaded,
                                             layer_name=layer_name_list[file_loaded - 1],layer_location=tmp_model.layer_location,layer_size = tmp_model.layer_size)
                        existing_models = model_dao.existing_models(db_model)
                        if len(existing_models) == 0:
                            model_dao.add_model(db_model)
        sql_data = DataInfo(model_name=obj_name_prefix, file_number=file_num, layer_number=len(layer_hash_list),
                            minio_count=minio_count, complete=1)
        data_dao.add_data(sql_data)
        return {"file_num": file_num, "file_loaded": file_loaded, "layer_hash_len": len(layer_hash_list),
                "minio_count": minio_count}
    except Exception as e:
        return {"error": "error: " + str(e)}

async def upload_(file: UploadFile):
    file_name = file.filename
    obj_name_prefix = os.path.splitext(file_name)[0]
    try:
        file_loaded = 0
        minio_count = 0
        disk_spaces = {}
        
        with TempDir() as tmp:
            base_path = tmp.path()
            file_path = os.path.join(base_path, file_name)
            model_path = os.path.join(base_path, "model")
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            loaded_model_state = torch.load(file_path, map_location='cpu')
            layer_name_list, layer_hash_list = utils._save_state_dict(state_dict=loaded_model_state, path=model_path)
            utils.common_layer_identification(layer_hash_list)
            files = list(os.scandir(model_path))
            file_num = len(files)
            for layer_hash in layer_hash_list:
                file_loaded += 1
                tmp_models = model_dao.get_model_by_layer_hash(layer_hash)
                if len(tmp_models) == 0:
                    disks = storage_dao.get_storage_all()
                    for disk in disks:
                        key = disk.minio_id + "_" + disk.minio_location
                        value = disk.free_space
                        disk_spaces[key] = value
                    file_size = os.path.getsize(model_path + "/" + layer_hash + ".pkl")
                    minio_id = utils.get_disk(file_size, disk_spaces)
                    if minio_id == "-1":
                        sql_data = DataInfo(model_name=obj_name_prefix, file_number=file_num,
                                            layer_number=len(layer_hash_list), minio_count=minio_count, complete=0)
                        data_dao.add_data(sql_data)
                        return {"error": "no space", "file_num": file_num, "file_loaded": file_loaded - 1,
                                "layer_hash_len": len(layer_hash_list),
                                "minio_count": minio_count}
                    client = utils.get_client(minio_id)
                    client.fput_object(bucket_name="test", object_name=obj_name_prefix + "/" + layer_hash + ".pkl",
                                       file_path=model_path + "/" + layer_hash + ".pkl")
                    storage = storage_dao.get_storage_by_minio_id(minio_id)
                    storage_dao.update_used_storage(file_size=file_size, storage=storage, minio_id=minio_id)
                    minio_count += 1
                    db_model_2 = ModelInfo_2(model_name=obj_name_prefix, layer_num=file_loaded, layer_hash=layer_hash,
                    layer_name=layer_name_list[file_loaded - 1])
                    model_dao.add_model_2(db_model_2)
                    db_location = LocationInfo(layer_hash=layer_hash, layer_location=obj_name_prefix, minio_id=minio_id)
                    model_dao.add_location(db_location)
                    
                else:
                    for tmp_model in tmp_models:
                        db_model_2 = ModelInfo_2(model_name=obj_name_prefix, layer_num=file_loaded, layer_hash=layer_hash,
                                             layer_name=layer_name_list[file_loaded - 1])
                        existing_models = model_dao.existing_models_2(db_model_2)
                        if len(existing_models) == 0:
                            model_dao.add_model_2(db_model_2)
        sql_data = DataInfo(model_name=obj_name_prefix, file_number=file_num, layer_number=len(layer_hash_list),
                            minio_count=minio_count, complete=1)
        data_dao.add_data(sql_data)
        return {"file_num": file_num, "file_loaded": file_loaded, "layer_hash_len": len(layer_hash_list),
                "minio_count": minio_count}
    except Exception as e:
        return {"error": "error: " + str(e)}

async def download(model_name: str, background_task: BackgroundTasks):
    try:
        hash_set = {}
        model = sorted(model_dao.get_model_by_model_name(model_name), key=lambda x: x.layer_number)
        folder_path = "/tmp/model"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        model_path = os.path.join(folder_path, model_name + ".pt")
        if model is None:
            return {"error": "no models"}
        with TempDir() as tmp:
            base_path = tmp.path()
            for layer in model:
                hash_set[layer.layer_name] = layer.layer_hash
                idx = layer.minio_id
                client = utils.get_client(idx)
                client.fget_object(bucket_name="test", object_name=layer.layer_location + "/" + layer.layer_hash + ".pkl",
                                   file_path=os.path.join(base_path, layer.layer_hash + ".pkl"))
            state_dict = utils.load_layer(hash_set, base_path)
            torch.save(state_dict, model_path)
        background_task.add_task(remove_file, model_path)
        
        return FileResponse(model_path, media_type="application/octet-stream", filename=model_name + '.pt')
    except Exception as e:
        return {"error": "error: " + str(e)}

async def download_(model_name: str, background_task: BackgroundTasks):
    try:
        hash_set = {}
        model = sorted(model_dao.get_model_by_model_name_2(model_name), key=lambda x: x.layer_num)
        folder_path = "/tmp/model"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        model_path = os.path.join(folder_path, model_name + ".pt")
        if model is None:
            return {"error": "no models"}
        with TempDir() as tmp:
            base_path = tmp.path()
            for layer in model:
                hash_set[layer.layer_name] = layer.layer_hash
                layer_location = "1"
                idx = layer_location.minio_id
                client = utils.get_client(idx)
                client.fget_object(bucket_name="test", object_name=layer_location.layer_location + "/" + layer.layer_hash + ".pkl",
                                   file_path=os.path.join(base_path, layer.layer_hash + ".pkl"))
            state_dict = model_compose.compose(hash_set, base_path)
            torch.save(state_dict, model_path)
        background_task.add_task(remove_file, model_path)
        
        return FileResponse(model_path, media_type="application/octet-stream", filename=model_name + '.pt')
    except Exception as e:
        return {"error": "error: " + str(e)}


async def delete_all():
    try:
        model_dao.delete_all()
        data_dao.delete_all()
        for i in range(1, 5):
            client = utils.get_client(str(i))
            objects = client.list_objects("test", prefix="", recursive=True)
            for obj in objects:
                client.remove_object("test", obj.object_name)
        storage_dao.refresh_storage()
        return {"result ": "delete"}
    except Exception as e:
        return {"error": str(e)}

async def delete_all_2():
    try:
        model_dao.delete_all_2()
        data_dao.delete_all()
        for i in range(1, 5):
            client = utils.get_client(str(i))
            objects = client.list_objects("test", prefix="", recursive=True)
            for obj in objects:
                client.remove_object("test", obj.object_name)
        storage_dao.refresh_storage()
        return {"result ": "delete"}
    except Exception as e:
        return {"error": str(e)}        
    
async def delete_by_model_name(model_name:str):
    try:           
        model_dao.delete_by_model_name(model_name)
        data_dao.delete_by_model_name(model_name)
        for i in range(1, 5):
            client = utils.get_client(str(i))
            objects = client.list_objects("test", prefix=model_name, recursive=True)
            for obj in objects:
                client.remove_object("test", obj.object_name)
        storage_dao.refresh_storage()
        return {"result ": "delete"}
    except Exception as e:
        return {"error": str(e)}
