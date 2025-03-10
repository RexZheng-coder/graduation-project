import requests
import torch
import os
import minio_test
from transformers import AutoImageProcessor, ResNetForImageClassification
from datasets import load_dataset
import mlflow
import mlflow.environment_variables
mlflow.environment_variables.MLFLOW_ENABLE_ARTIFACTS_PROGRESS_BAR.default = False
from mlflow.pytorch import load_state_dict, _load_state_dict, _load_state_dict_2

mlflow.set_tracking_uri("http://172.17.0.1:5001")

def main(args):
    state_dict_uri = "mlflow-artifacts:/1/c1d6ce8641cf4a55a4c0496319fe556c/artifacts"
    state_dict = _load_state_dict_2(state_dict_uri)
    
    try:
        os.makedirs("/tmp/resnet", exist_ok=True)
        path = "/tmp/resnet/pytorch_model.bin"
        torch.save(state_dict, path)
        config_url = "https://huggingface.co/microsoft/resnet-50/resolve/main/config.json"
        res = requests.get(config_url)
        res.raise_for_status()
        with open("/tmp/resnet/config.json", "wb") as f:
            f.write(res.content)
        try:
            dataset = load_dataset("huggingface/cats-image")
            image = dataset["test"]["image"][0]
            processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
            model = ResNetForImageClassification.from_pretrained("/tmp/resnet/")
            inputs = processor(image, return_tensors="pt")
            with torch.no_grad():
                logits = model(**inputs).logits
            predicted_label = logits.argmax(-1).item()
            return {"Predicted class:": model.config.id2label[predicted_label]}
        except FileNotFoundError:
            return {"error": "Model file not found"}
        except RuntimeError as e:
            return {"error": str(e)}
    except Exception as e:
        return {"erro":str(e)}