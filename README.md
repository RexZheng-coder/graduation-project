# Graduation Project Workspace

This repository is the full working directory for my graduation project on fine-grained DNN model storage for serverless edge inference.

The main engineering deliverable is in `Re2po/`, which contains the Re2po prototype and its supporting service code. Everything else in the repository is now grouped by purpose so the workspace is easier to navigate and maintain.

## Directory Guide

```text
Re2po/         Core system prototype and service implementation
docs/          Paper and reference material
experiments/   Training, serialization, and MLflow exploration code
datasets/      Local raw dataset copies used by experiments
artifacts/     Generated model files, checkpoints, and tracking outputs
environments/  Dockerfiles and environment snapshots
```

## Where To Start

- Read `Re2po/README.md` for the main project.
- Use `experiments/` to inspect earlier prototype work and MLflow examples.
- Treat `artifacts/` and `datasets/` as local research materials, not polished deliverables.

## Notes

- The repository keeps historical experiment outputs because they document how the project evolved.
- Cache folders such as `__pycache__` and notebook checkpoint directories are intentionally excluded from the organized layout.
