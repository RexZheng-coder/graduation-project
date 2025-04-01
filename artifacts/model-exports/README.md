# Model Exports

This directory contains saved model files and related metadata produced while testing model storage and reconstruction workflows.

## Contents

- `.pth`, `.pt`, and `.pkl` files are example exported model artifacts.
- `hash_info.txt` captures hash-related metadata generated during decomposition experiments.
- `.txt` files describe or accompany stored model outputs used during prototype debugging.

## Role In The Project

These files are the small-scale, concrete objects that sit underneath the larger Re2po idea. Before a repository service can store and reconstruct models across nodes, someone has to inspect actual exported artifacts and understand what they look like in practice. This directory preserves that part of the process.
