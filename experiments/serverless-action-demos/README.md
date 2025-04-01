# Serverless Action Demos

This directory contains lightweight Python action-style scripts used while exploring how model-related logic might behave inside a serverless runtime.

## Files

- `hello.py` is a minimal action example used to verify function execution and runtime information.
- `test.py` is a small action variant that inspects the Python runtime and MLflow import location.
- `mlflow_test.py` extends that idea by querying an MLflow tracking server from a function-style entrypoint.

## Why This Directory Exists

Re2po is motivated by serverless edge inference, so it was useful to validate a few basics early:

- what a Python action entrypoint should look like,
- how dependencies appear at runtime,
- and whether an action can talk to external tracking infrastructure such as MLflow.

These files are intentionally small. Their value is in environment exploration, not in application complexity.
