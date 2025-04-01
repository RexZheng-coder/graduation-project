# Training Checkpoints

This directory contains checkpoint files produced by local training runs.

## Contents

- `epoch=2-step=1290.ckpt` is a standalone checkpoint snapshot.
- `training_1/` contains TensorFlow-style checkpoint files captured during an earlier run.

## Why They Were Kept

Checkpoint files were useful during debugging because they made it possible to inspect intermediate model states and compare storage formats across frameworks and workflows.
