import os
import numpy as np
from collections import OrderedDict
import tensorflow as tf

def read(file_path):
    model_shape = {}
    model_hash = {}

    with open(file_path, 'r') as file:
        for line in file:
            state = line[1]
            line = line[3:]
            line = line.strip()
            parts = line.split(':')
            layer = parts[0]
            data = parts[1][1:-1].split(',')
            match state:
                case 's':  # Shape
                    layer_shape = []
                    for i in data:
                        layer_shape.append(int(i))
                    model_shape[layer] = layer_shape

                case 'p':  # Parameters
                    hash_value = []
                    for i in data:
                        hash_value.append(i.strip()[1:-1])
                    model_hash[layer] = hash_value
    return model_shape, model_hash

def load_block(hash_value, data_path, meth="tensorflow"):
    block_path = os.path.join(data_path, hash_value)
    if meth == "hdf5":
        block_path += ".h5"
        with h5py.File(block_path, 'r') as hf:
            block = np.array(hf['weights'])
    elif meth == "pickle":
        block_path += ".pkl"
        with open(block_path, 'rb') as file:
            block = pickle.load(file)
    elif meth == "tensorflow":
        block_path += ".tf.npy"
        block = np.load(block_path)
    return block

def compose(file_path, data_path, meth="tensorflow"):
    _, model_hash = read(file_path)
    model_state = {}
    for layer_name, hash_values in model_hash.items():
        if len(hash_values) == 1:  # Single weight
            model_state[layer_name] = load_block(hash_values[0], data_path, meth)
        else:  # Multiple weights (e.g., kernel and bias)
            layer_weights = [load_block(hash_value, data_path, meth) for hash_value in hash_values]
            model_state[layer_name] = layer_weights
    model_state = OrderedDict(model_state)
    return model_state

def restore_model(file_path, data_path, output_model_path, meth="tensorflow"):
    model_weights = compose(file_path, data_path, meth)

    # Recreate the model based on the loaded weights
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(10,)),
        tf.keras.layers.Dense(20, activation='relu'),
        tf.keras.layers.Dense(30, activation='relu'),
        tf.keras.layers.Dense(5, activation='softmax')
    ])
    
    # Set the loaded weights into the model
    for layer in model.layers:
        if layer.name in model_weights:
            layer.set_weights(model_weights[layer.name])
    
    # Save the restored model
    model.save(output_model_path, save_format="keras")

def test():
    data_path = "./block_files"
    loaded_model_path = "./tensorflow_model.txt"
    output_model_path = "./restored_model.keras"
    restore_model(loaded_model_path, data_path, output_model_path, meth="tensorflow")

if __name__ == "__main__":
    test()