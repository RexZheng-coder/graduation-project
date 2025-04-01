# Tracking Outputs

This directory contains experiment tracking outputs produced while testing training and logging workflows.

## Contents

- `mlruns/` stores MLflow tracking artifacts and metadata.
- `lightning_logs/` stores PyTorch Lightning logs and summaries.

## Why This Directory Matters

Tracking outputs are not just clutter in this project. They document how experiments were run, what metrics were logged, and what artifacts were emitted. That context is useful when connecting experiment code in `experiments/` with the storage and repository ideas that matured into Re2po.
