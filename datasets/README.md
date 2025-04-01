# Datasets

This directory stores local raw datasets used by the experiments in this repository.

These are kept outside the main `Re2po/` implementation because they support experimentation rather than the service itself.

## Contents

- `fashion-mnist/` contains the raw FashionMNIST files.
- `mnist/` contains the raw MNIST files.

## Why The Data Is Preserved

- The experiment folders reference these datasets directly.
- Keeping the raw files locally makes the historical experiments easier to rerun.
- Storing them here keeps the top-level repository layout cleaner than scattering dataset folders across experiment directories.

## Practical Note

These files are local research inputs, not a custom dataset produced by the project. They are included here for convenience and traceability.
