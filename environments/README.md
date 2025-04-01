# Environments

This directory stores environment setup material collected during the project.

The files here are less about the final system design and more about the practical reality of getting experiments and service prototypes to run across different machines and container contexts.

## Structure

- `docker/` contains Docker build contexts and runtime image experiments.
- `snapshots/` contains captured Python environment snapshots from development.

## Why This Directory Exists

Graduation projects tend to accumulate environment knowledge in scattered files. Pulling that material into one place makes the repository easier to reason about and keeps setup history available without mixing it into the main source tree.
