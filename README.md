# Re2po Workspace

This repository is the full working workspace for my graduation project on fine-grained DNN model storage for serverless edge inference. It keeps the planning document, the thesis paper, the final system prototype, and the supporting experiments that led to it, so the structure reflects how the project evolved rather than only the polished end result.

The repository itself is the outer Re2po workspace. The main service implementation lives in the inner `Re2po/` directory, which contains the redundancy-aware model repository prototype for edge serverless computing. The surrounding directories preserve the planning paper, the thesis paper, the training experiments, the model decomposition scripts, the local datasets, the exported artifacts, and the environment snapshots that supported the thesis work.

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

1. Start with `docs/README.md` if you want the project in its real chronological order.
2. Read `docs/paper/serverless_inference_planning_paper.pdf` first to see the earlier planning-stage framing.
3. Read `docs/paper/re2po_paper.pdf` next to see how that framing turned into the named Re2po system design.
4. Move to `Re2po/README.md` for the implementation-oriented view.
5. Browse `experiments/README.md` to see how the storage idea was explored and validated.
6. Use `artifacts/README.md` and `datasets/README.md` as inventory guides for local materials.

## Project Timeline

This workspace follows the actual order in which the project matured:

1. The planning paper came first and framed the broader problem of fine-grained DNN model repository design for serverless AI inference.
2. The Re2po paper came next and narrowed that broader problem into a more concrete redundancy-aware repository design.
3. The inner `Re2po/` codebase represents the prototype implementation stage that followed those papers.
4. The `experiments/` and `artifacts/` directories preserve the technical exploration around that implementation.

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
- Planning paper: `docs/paper/serverless_inference_planning_paper.pdf`
- Thesis paper copy: `docs/paper/re2po_paper.pdf`
- MLflow experiment area: `experiments/mnist-mlflow/`
- Model storage prototypes: `experiments/model-storage-prototypes/`
- Environment snapshots: `environments/snapshots/`
