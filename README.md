# Typed Decision Layer

> **Local private review:** publication is paused. See [security review and remaining release conditions](docs/SECURITY_REVIEW.md). Local fixes have not been pushed.


A local decision integration layer with typed answers, versioned policies, evidence and persistent decision records.

![review](https://img.shields.io/badge/review-private-374151) ![primary](https://img.shields.io/badge/primary-Python-2563EB) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Douglas%20Silva-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/douglas-silva-data-analyst/)

[Overview](#overview) · [Architecture](#architecture) · [Setup](#setup) · [Validation](#validation) · [Roadmap](#roadmap) · [Review notes](docs/REVIEW.md)

## Overview

- Typed answer contracts connect model output to policies and evidence.
- Revision pinning and local runtime configuration make inference inputs inspectable.
- Integration code extends the upstream Laya project while retaining its attribution.

**Technology:** Python · PyTorch · Transformers · safetensors · SQLite · TypeScript client · optional FastAPI/ONNX integrations

**Persistence and data:** SQLite ledger and revision metadata support decision lineage. Model checkpoints are external assets and are not bundled.

## Architecture

```text
Pinned checkpoint and typed request → local inference → output/policy validation → durable decision record
```

| Location | Review focus |
| --- | --- |
| [`laya`](laya) | Source/configuration inspected for scope and structure |
| [`laya-ts`](laya-ts) | Source/configuration inspected for scope and structure |
| [`OMNIA_NOTICES.md`](OMNIA_NOTICES.md) | Source/configuration inspected for scope and structure |
| [`UPSTREAM_README.md`](UPSTREAM_README.md) | Source/configuration inspected for scope and structure |
| [`pyproject.toml`](pyproject.toml) | Source/configuration inspected for scope and structure |

Internal package and module names are retained where changing them would affect imports or compatibility. This descriptive repository name does not imply a completed package/API migration.

## Setup

Read pyproject.toml optional extras and CONTRIBUTING.md before installation. Install only the backend needed for your environment; GPU and ONNX paths require separate validation.

Start from an isolated environment. Use `.env.example` when present and inspect the configuration loader: an example file is not necessarily loaded automatically. Runtime databases, real account sessions and private credentials are not bundled. Live integration prerequisites are separate from local tests.

## Validation

Static parsing checked 134 Python files and 37 strict JSON files. Python syntax errors: 0; JSON errors: 0. No functional test/build result is claimed for this preparation. Additional gates: ruff — passed: E9,F63,F7,F82,F401,F811; compileall — passed: laya and tests; model_runtime — not executed.

Available test scripts are inventoried in [the review notes](docs/REVIEW.md). Choose offline checks before operating any integration.

These results apply to the selected checks on the preparation copy. They do not establish deployment readiness, full coverage, live provider availability or measured performance. CI definitions, when present under `docs/ci-templates/`, are inactive review templates; no remote CI badge is claimed.

## Limits and current status

This is an integration fork of upstream Laya, not an independently authored inference engine. Torch, optional runtimes and checkpoints were not installed or executed in this review. Historical benchmark files are not fresh measurements.

This private snapshot is for code and portfolio review. Generated runtime material and unreviewed binary assets may be excluded. [Review notes](docs/REVIEW.md) record preparation scope, findings and outstanding validation.

## Roadmap

- [ ] Run the repository's required Ruff and compile gates.
- [ ] Test the integration layer with controlled answers before loading a model.
- [ ] Validate the TypeScript client and chosen optional runtime separately.

## History and attribution

392 existing commits were retained after path/content filtering. Original authors and author/committer dates were retained; commit hashes may change. Upstream commits are not presented as new work by the maintainer.

Existing license and attribution files are retained: [LICENSE](LICENSE). Review their scope and third-party notices before redistribution.

## Maintainer and feedback

Douglas de Oliveira Silva · [GitHub](https://github.com/qquante) · [LinkedIn](https://www.linkedin.com/in/douglas-silva-data-analyst/)

For this private review, report reproducible issues with a minimal fixture and the exact check output. Keep account data, credentials and generated sensitive reports out of issues and commits. Existing contribution guidelines apply where present.

**Topics:** `python`, `pytorch`, `transformers`, `structured-output`, `local-ai`, `sqlite`, `typescript`
