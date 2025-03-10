# Re2po

A Distributed Redundancy-aware Model Repository for Edge Serverless Computing.

Re2po is the core system prototype behind the thesis project "Re2po: A Distributed Redundancy-aware Model Repository in Edge Serverless Computing". It targets the model-loading bottleneck in edge serverless machine learning: large DNN weights are expensive to repeatedly fetch, duplicate, and move across constrained edge storage nodes.

The project explores a fine-grained storage design for PyTorch and TensorFlow models. Instead of treating a trained model as one opaque file, Re2po decomposes model state into layer-level objects, identifies duplicate layers by content hash, places unique layer objects across MinIO-backed storage nodes, and reconstructs the full model state transparently for inference functions.

## Architecture

```text
Client / serverless function
        |
        v
FastAPI gateway
        |
        v
Model storage service
        |
        +-- Layer decomposition and hash-based redundancy detection
        +-- Metadata access through MySQL / Redis DAO modules
        +-- Distributed layer object storage through MinIO
        +-- Model reconstruction for download / inference
        |
        v
OpenWhisk / Kubernetes deployment experiments
```

## Project Structure

```text
deps/
├── docker-compose.yml                  # Local MinIO, MySQL, and Redis dependencies
└── openwhisk-deploy-kube-extra-files/  # OpenWhisk / Kubernetes deployment experiments

lib/
└── requirements.txt                    # Python runtime dependencies

src/
├── dao/                                # MySQL / Redis metadata access layer
├── gateway/                            # FastAPI API gateway
├── model/                              # SQLAlchemy metadata entities
├── services/                           # Model decomposition, storage, and reconstruction logic
└── utils/                              # MinIO client selection and layer utility functions
```

## Core Ideas

- Redundancy-aware storage: layer tensors are serialized and addressed by SHA-256 hashes so identical layers can be stored once and referenced by multiple models.
- Fine-grained DNN model management: PyTorch `state_dict` and TensorFlow model weights are decomposed into layer objects instead of uploaded as monolithic files.
- Distributed edge storage: MinIO instances simulate multiple edge storage nodes, while metadata tables track model-to-layer and layer-to-location relationships.
- Serverless-oriented access: FastAPI exposes upload, download, and cleanup endpoints intended to sit in front of OpenWhisk actions or other inference functions.
- Recomposition on demand: download APIs fetch required layer objects, rebuild the model state, and return a complete model artifact to the caller.

## Runtime Dependencies

Install the Python dependencies from:

```sh
pip install -r lib/requirements.txt
```

Start the local backing services from this directory:

```sh
docker compose -f deps/docker-compose.yml up -d
```

The code reads runtime settings from environment variables. Copy `.env.example` when you need a local reference:

```sh
cp .env.example .env
```

Important configuration keys:

```text
RE2PO_DATABASE_URL=mysql+pymysql://root:mysql_pwd@localhost:3306/minio?charset=utf8mb4
RE2PO_REDIS_HOST=localhost
RE2PO_REDIS_PORT=6379
RE2PO_MINIO_1_ENDPOINT=localhost:9010
RE2PO_MINIO_1_ACCESS_KEY=minio_user
RE2PO_MINIO_1_SECRET_KEY=minio_pwd
```

## API Surface

The gateway exposes the following prototype endpoints:

```text
POST /minio/upload       Upload a model and store unique layer objects.
POST /minio/download     Reconstruct and download a stored model.
POST /minio/delete       Delete metadata for one model.
POST /minio/delete_all   Clear model metadata.
```

The `_` suffixed endpoints are earlier variants that split model metadata and layer location metadata into separate tables.

## Engineering Notes / Known Gaps

This repository is a thesis prototype that has been cleaned for portfolio review. The most important remaining engineering work is:

- Replace prototype-wide DAO sessions with request-scoped SQLAlchemy sessions.
- Add database migrations and schema bootstrapping for the metadata tables.
- Finish configuration hardening for production MinIO credentials and bucket creation.
- Consolidate the two upload/download API variants into one stable interface.
- Add stronger error handling around partial uploads, storage exhaustion, and failed layer reconstruction.
- Separate OpenWhisk experiment files from the core Python package when preparing a production release.

## Resume Framing

Re2po is best described as a distributed, redundancy-aware DNN model repository for edge serverless inference. The project demonstrates model artifact decomposition, content-addressed storage, metadata-driven reconstruction, and integration work across FastAPI, MinIO, MySQL, Redis, Docker, Kubernetes, and OpenWhisk.
