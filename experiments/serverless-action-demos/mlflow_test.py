import mlflow
import sys
# Use the fluent API to set the tracking uri and the active experiment

def main(dict):
    if 'name' in dict:
        name = dict['name']
    else:
        name = "stranger"
    greeting = "Hello " + name + "!"
    version = sys.version
    mlflow_pos = mlflow.__file__
    mlflow.set_tracking_uri("http://host.docker.internal:5001")
    client = mlflow.MlflowClient(tracking_uri="http://host.docker.internal:5001")
    all_experiments = client.search_experiments()
    print(all_experiments)
    print(greeting)
    print(version)
    print(mlflow_pos)
    print(str(all_experiments))
    return {"greeting": greeting, "version": version, "mlflow":mlflow_pos,
            "all_experiments": str(all_experiments)}

main({'name':'world'})