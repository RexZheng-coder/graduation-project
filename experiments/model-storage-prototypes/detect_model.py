import torch
import joblib
import pickle
import tensorflow as tf

def detect_framework(model_path):
    # 尝试使用 PyTorch 加载模型
    try:
        torch.load(model_path)
        return "PyTorch"
    except (AttributeError, RuntimeError, pickle.UnpicklingError):
        pass

    # 尝试使用 TensorFlow 加载模型
    try:
        tf.keras.models.load_model(model_path)
        return "TensorFlow"
    except (ValueError, AttributeError, OSError, EOFError):
        pass

    # 尝试使用 joblib 或者 pickle 加载模型
    try:
        with open(model_path, 'rb') as file:
            joblib.load(file)
        return "Scikit-learn"
    except (ValueError, AttributeError, OSError, EOFError, pickle.UnpicklingError, KeyError):
        pass

    return "Unknown"


if __name__ == "__main__":
    # 使用 detect_framework 函数判断模型类型
    model_path = '../model.pkl'  # 替换成你的模型文件路径
    framework = detect_framework(model_path)
    print(f"The model is using: {framework}")
