# Model Storage Prototypes

This directory contains the early scripts and notebooks used to explore model decomposition, hashing, serialization, and recomposition before those ideas were folded into Re2po.

## What Lives Here

- `model_save.py` and `model_compose.py` focus on PyTorch model decomposition and recomposition.
- `detect_model.py` explores model type detection.
- `torch_compose.py`, `test1.py`, and `test2.py` are smaller exploratory scripts around model reconstruction and storage behavior.
- The notebooks preserve ad hoc experiments for PyTorch, TensorFlow, and MLflow behavior.
- `pytorch_model.txt` is a local sample artifact used while testing model metadata output.

## Why This Directory Matters

This folder shows the project before it became a service:

- first, understand how a model can be split into meaningful units,
- then, verify that those units can be hashed and stored,
- and only after that move toward a repository service such as Re2po.

That makes this directory useful when you want to explain the engineering evolution of the project, not just the final architecture.

## Caveats

- The scripts here are exploratory and not packaged as a stable library.
- Some files overlap conceptually with logic that later moved into `Re2po/src/services/`.
- Notebook-heavy workflows are preserved for traceability, not because they are the final form of the implementation.
