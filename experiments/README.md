# Experiments

This directory contains the exploratory and intermediate work that informed the final Re2po prototype. It is the bridge between the polished system in `Re2po/` and the smaller scripts, notebooks, and experiments that helped shape it.

## Structure

- `mnist-mlflow/` contains a self-contained training and tracking example built around MNIST, MLflow, and PyTorch Lightning.
- `model-storage-prototypes/` contains earlier scripts that explore model hashing, decomposition, serialization, and reconstruction.
- `serverless-action-demos/` contains lightweight action-style scripts used while exploring serverless execution environments.

## How These Experiments Relate To Re2po

- `mnist-mlflow/` helped validate experiment tracking and model packaging workflows.
- `model-storage-prototypes/` contains the early logic that eventually informed the layer-level storage ideas used by Re2po.
- `serverless-action-demos/` captures the environment assumptions behind running Python code inside a serverless-style function context.

## Reading Advice

- Start with `model-storage-prototypes/` if you want to understand the storage idea from the bottom up.
- Start with `mnist-mlflow/` if you want a concrete training-and-logging example.
- Treat these folders as research history: they are useful, but they are less polished than the main implementation.
