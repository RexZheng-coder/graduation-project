# Environment Snapshots

This directory stores captured environment manifests from development.

## Contents

- `env_a_requirements.txt` is a pip-style package snapshot.
- `env_a_conda.yml` is a Conda environment snapshot.

## Why They Were Kept

These files preserve the dependency context of earlier experiments. They are useful when reconstructing the working environment behind notebooks, MLflow runs, or prototype scripts whose dependencies later drifted.
