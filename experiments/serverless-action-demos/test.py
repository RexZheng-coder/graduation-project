import sys
import mlflow
def main(dict):
    if 'name' in dict:
        name = dict['name']
    else:
        name = "stranger"
    greeting = "Hello " + name + "!"
    version = sys.version
    mlflow_pos = mlflow.__file__
    print(greeting)
    print(version)
    print(mlflow_pos)
    return {"greeting": greeting, "version": version, "mlflow":mlflow_pos}

