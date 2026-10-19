# Typed Decision Layer

A local decision integration layer with typed answers, versioned policies, evidence and persistent decision records.

## Features

- Typed answer contracts connect model output to policies and evidence.
- Revision pinning and local runtime configuration make inference inputs inspectable.
- Integration code extends the upstream Laya project while retaining its attribution.

## Stack

Python · PyTorch · Transformers · safetensors · SQLite · TypeScript client · optional FastAPI/ONNX integrations

SQLite ledger and revision metadata support decision lineage. Model checkpoints are external assets and are not bundled.

## Getting started

Read pyproject.toml optional extras and CONTRIBUTING.md before installation. Install only the backend needed for your environment; GPU and ONNX paths require separate validation.

## How it works

```text
Pinned checkpoint and typed request → local inference → output/policy validation → durable decision record
```

## Current limitations

This is an integration fork of upstream Laya, not an independently authored inference engine. Torch, optional runtimes and checkpoints were not installed or executed in this review. Historical benchmark files are not fresh measurements.

## Attribution

Based on Laya. Preserve the upstream license, notices and author attribution included in this repository.

## License

See [LICENSE](LICENSE), [OMNIA_NOTICES.md](OMNIA_NOTICES.md).
