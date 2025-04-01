# Docker Environments

This directory contains Docker-related build contexts used during project development.

## Contents

- `base-runtime/` contains a general Docker environment used for Python-based experimentation.
- `openwhisk-py11/` contains a Python 3.11 image variant used while exploring OpenWhisk-style execution.
- `openwhisk-py11-mlflow/` contains a Python 3.11 image variant with MLflow-related runtime needs in mind.

## Role In The Workspace

These Dockerfiles capture the runtime side of the project: not only how the code works on a laptop, but how it might be packaged into a more controlled execution environment for serverless or containerized use.
