import redis
import json
import os

r = redis.Redis(
    host=os.getenv('RE2PO_REDIS_HOST', 'localhost'),
    port=int(os.getenv('RE2PO_REDIS_PORT', '6379')),
    decode_responses=True,
)


def add_data(data):
    try:
        r.hset(f"data:{data.model_name}", mapping={
            "file_number": data.file_number,
            "layer_number": data.layer_number,
            "minio_count": data.minio_count,
            "complete": data.complete
        })
    except Exception as e:
        return {"error": str(e)}

def delete_all_data():
    try:
        for key in r.scan_iter("data:*"):
            r.delete(key)
    except Exception as e:
        return {"error": str(e)}

def delete_data_by_model_name(model_name):
    try:
        r.delete(f"data:{model_name}")
    except Exception as e:
        return {"error": str(e)}

def add_model(model):
    try:
        key = f"model:{model.model_name}"
        layer_info = {
            "layer_hash": model.layer_hash,
            "layer_name": model.layer_name,
            "layer_number": model.layer_number,
            "minio_id": model.minio_id,
            "layer_location": model.layer_location,
            "layer_size": model.layer_size
        }
        r.rpush(key, json.dumps(layer_info))
        r.sadd(f"layer:{model.layer_hash}", model.model_name)
        r.hset(f"layer_info:{model.model_name}:{model.layer_number}", mapping=layer_info)
    except Exception as e:
        return {"error": str(e)}

def add_model_2(model):
    try:
        key = f"model:{model.model_name}"
        layer_info = {
            "layer_hash": model.layer_hash,
            "layer_name": model.layer_name,
            "layer_number": model.layer_num
        }
        r.rpush(key, json.dumps(layer_info))
        r.sadd(f"layer:{model.layer_hash}", model.model_name)
        r.hset(f"layer_info:{model.model_name}:{model.layer_num}", mapping=layer_info)
    except Exception as e:
        return {"error": str(e)}

def existing_models(model):
    try:
        key = f"layer_info:{model.model_name}:{model.layer_number}"
        stored = r.hgetall(key)
        return [stored] if stored and stored.get("layer_hash") == model.layer_hash else []
    except Exception as e:
        return {"error": str(e)}

def existing_models_2(model):
    try:
        key = f"layer_info:{model.model_name}:{model.layer_num}"
        stored = r.hgetall(key)
        return [stored] if stored and stored.get("layer_hash") == model.layer_hash else []
    except Exception as e:
        return {"error": str(e)}

def get_model_by_layer_hash(layer_hash):
    try:
        return list(r.smembers(f"layer:{layer_hash}"))
    except Exception as e:
        return {"error": str(e)}

def get_model_by_model_name(model_name):
    try:
        entries = r.lrange(f"model:{model_name}", 0, -1)
        return [json.loads(e) for e in entries]
    except Exception as e:
        return {"error": str(e)}

def delete_all_models():
    try:
        for key in r.scan_iter("model:*"):
            r.delete(key)
        for key in r.scan_iter("layer:*"):
            r.delete(key)
        for key in r.scan_iter("layer_info:*"):
            r.delete(key)
    except Exception as e:
        return {"error": str(e)}

def delete_by_model_name(model_name):
    try:
        layers = get_model_by_model_name(model_name)
        for layer in layers:
            r.srem(f"layer:{layer['layer_hash']}", model_name)
            r.delete(f"layer_info:{model_name}:{layer['layer_number']}")
        r.delete(f"model:{model_name}")
        delete_data_by_model_name(model_name)
    except Exception as e:
        return {"error": str(e)}
