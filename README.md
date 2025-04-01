# Re2po Workspace

This repository is the full working workspace for my graduation project on fine-grained DNN model storage for serverless edge inference. It keeps both the final system prototype and the supporting experiments that led to it, so the structure reflects how the project was actually built rather than only the polished end result.

The repository itself is the outer Re2po workspace. The main service implementation lives in the inner `Re2po/` directory, which contains the redundancy-aware model repository prototype for edge serverless computing. The surrounding directories preserve the training experiments, model decomposition scripts, local datasets, exported artifacts, and environment snapshots that supported the thesis work.

## Repository Map

```text
Re2po/         Main service implementation and prototype source code
docs/          Paper and project reference material
experiments/   Prototype code, training experiments, and exploratory scripts
datasets/      Local raw dataset copies used by the experiments
artifacts/     Generated models, checkpoints, and tracking outputs
environments/  Docker build context and captured environment snapshots
```

## Recommended Reading Order

1. Start with `Re2po/README.md` to understand the main problem, architecture, and service design.
2. Read `docs/README.md` if you want the thesis context and paper-facing material.
3. Browse `experiments/README.md` to see how the storage idea was explored and validated.
4. Use `artifacts/README.md` and `datasets/README.md` as inventory guides for local materials.

## What This Workspace Contains

- A service prototype that decomposes neural network models into layer-level objects and reconstructs them on demand.
- MLflow and PyTorch Lightning experiments used to study training metadata and model packaging.
- Early scripts for PyTorch and TensorFlow model serialization, hashing, and recomposition.
- Local copies of MNIST and FashionMNIST data used during experimentation.
- Checkpoints, exported model files, and tracking logs kept for traceability.

## Notes On Organization

- The inner `Re2po/` directory is the deliverable-quality part of the repository.
- `experiments/` is intentionally preserved as research history, so some files are rougher and more exploratory.
- `artifacts/` and `datasets/` are useful for reproduction and inspection, but they are supporting materials rather than the main project narrative.
- Cache folders and notebook checkpoint folders are intentionally excluded from the organized layout.

## Quick Navigation

- Main implementation: `Re2po/`
- Thesis paper copy: `docs/paper/re2po_paper.pdf`
- MLflow experiment area: `experiments/mnist-mlflow/`
- Model storage prototypes: `experiments/model-storage-prototypes/`
- Environment snapshots: `environments/snapshots/`
