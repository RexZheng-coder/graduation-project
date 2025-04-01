# MNIST MLflow Experiment

This directory contains a compact training-and-tracking experiment built around MNIST, PyTorch Lightning, and MLflow. Its role in the larger workspace is to preserve the experiment path that helped connect model training, artifact logging, and reproducible metadata capture.

## Purpose

The experiment answers a practical question that matters for Re2po: once a model is trained, how should its parameters, metrics, and serialized outputs be tracked so that storage and reconstruction work can be inspected later?

## Main Files

- `mnist_autolog_example.py` is the main training script.
- `MLproject` defines the MLflow project entry.
- `conda.yaml`, `python_env.yaml`, and `example2/python_env.yaml` capture environment variants used while running the experiment.
- `mlruns/` stores recorded MLflow runs.
- `lightning_logs/` stores PyTorch Lightning outputs.
- `epoch=*.ckpt` files are training checkpoints preserved as local artifacts.
- `dataset/` stores the local MNIST copy used by the run.

## Typical Workflow

Run through MLflow:

```sh
mlflow run . --env-manager=local
```

Run with custom parameters:

```sh
mlflow run . --env-manager=local -P max_epochs=5
```

Run the script directly:

```sh
python mnist_autolog_example.py \
  --trainer.max_epochs 5 \
  --trainer.devices 1 \
  --trainer.accelerator cpu \
  --data.batch_size 64 \
  --data.num_workers 2 \
  --model.learning_rate 0.001
```

Inspect tracking output:

```sh
mlflow ui
```

## Why This Folder Was Kept

This experiment is simpler than Re2po, but it preserves a useful part of the project story:

- how model artifacts were logged,
- how training metadata was captured,
- and how experiment outputs accumulated before the final storage system took shape.

In other words, this is not the product itself. It is part of the evidence trail behind the product.
