import h5py
import pickle
import os
import hashlib
import numpy as np
import tensorflow as tf
from tensorflow.keras import Input

def hash_cal(weights):
    block = weights
    block_hash = hashlib.sha256(block.tobytes()).hexdigest()
    return block_hash

def save_block(block, dirs, meth="hdf5", **kwargs):
    file_path = hash_cal(block)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    if meth == 'hdf5':
        file_name = os.path.join(dirs, file_path + ".h5")
        if not os.path.exists(file_name):
            with h5py.File(file_name, 'w') as hf:
                hf.create_dataset('weights', data=block)

    elif meth == 'pickle':
        file_name = os.path.join(dirs, file_path + ".pkl")
        if not os.path.exists(file_name):
            with open(file_name, 'wb') as file:
                pickle.dump(block, file, **kwargs)

    elif meth == "tensorflow":
        file_name = os.path.join(dirs, file_path + ".tf")
        if not os.path.exists(file_name):
            np.save(file_name, block)

    return file_path

def save_weights(info_path, layer_name, dirs, weights, block_size=5, dim_used=2):
    weights_shape = {}
    hash_table = []
    for i in range(len(weights.shape)):
        weights_shape[i] = weights.shape[i]

    hash_table.append(save_block(weights, dirs))

    with open(info_path, 'a') as file:
        file.write("[p]")
        file.write(f"{layer_name}:{hash_table}\n")

def save_model(dirs, loaded_model_path):
    # 加载模型
    model = tf.keras.models.load_model(loaded_model_path)
    info_path = os.path.splitext(os.path.basename(loaded_model_path))[0] + ".txt"

    # 用 w 模式清空文件
    if not os.path.exists(info_path):
        open(info_path, 'w').close()
    else:
        with open(info_path, 'a+') as file:
            file.truncate(0)

    for layer in model.layers:
        layer_name = layer.name
        weights = layer.get_weights()
        if weights:  # 检查是否有权重
            for i, weight in enumerate(weights):
                weight_name = f"{layer_name}_weight_{i}"
                with open(info_path, 'a') as file:
                    file.write("[s]")
                    file.write(f"{weight_name}:{list(weight.shape)}\n")
                save_weights(info_path, weight_name, dirs, weight)

def save_info(dirs, state_dict, **kwargs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    info_path = os.path.join(dirs, "model_info.txt")
    if not os.path.exists(info_path):
        open(info_path, 'w').close()
    else:
        with open(info_path, 'a+') as file:
            file.truncate(0)

    for k, v in state_dict.items():
        hash_table = []
        hash_table.append(hash_cal(v))
        with open(info_path, 'a') as file:
            file.write("[s]")
            file.write(f"{k}:{list(v.shape)}\n")
            file.write("[p]")
            file.write(f"{k}:{hash_table}\n")

def save_state_dict(dirs, state_dict, **kwargs):
    for k, v in state_dict.items():
        save_block(block=v, dirs=dirs, **kwargs)

def test():
    model = tf.keras.Sequential([
    Input(shape=(10,)),
    tf.keras.layers.Dense(20, activation='relu'),
    tf.keras.layers.Dense(30, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')
])
    model.save("./tensorflow_model.keras", save_format="keras")

    # 加载已保存的模型并存储权重
    dirs = "./block_files"
    loaded_model_path = "./tensorflow_model.keras"
    save_model(dirs, loaded_model_path)

if __name__ == "__main__":
    test()