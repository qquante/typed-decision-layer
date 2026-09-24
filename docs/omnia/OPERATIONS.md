# Run OMNIA Laya

Use Python 3.10 or newer. Clone this repository, create a virtual environment,
install a PyTorch build for the target device, then install the local checkout:

```bash
python -m pip install -e .
```

The integration invokes Laya in the local process. Model weights are downloaded
from Hugging Face on first use and cached; subsequent inference can run offline.
Select a reviewed immutable commit from the
[checkpoint history](https://huggingface.co/convaiinnovations/laya/commits/main).

## Configuration

The full template is `examples/omnia/.env.example`. Export values into the process
environment; the command does not automatically load dotenv files.

| Variable | Default | Purpose |
| --- | --- | --- |
| `OMNIA_LAYA_REVISION` | Required | Full 40-character checkpoint commit |
| `OMNIA_LAYA_MODEL` | `english` | `english`, `multilingual`, or `typed-decisions` |
| `OMNIA_LAYA_DEVICE` | `cpu` | CPU, CUDA or MPS |
| `OMNIA_LAYA_THREADS` | `2` | CPU intra-op threads, 1–64 |
| `OMNIA_LAYA_MAX_LEN` | `512` | Total token budget; checkpoint-specific maximum |
| `OMNIA_LAYA_HEAD_MAX_LEN` | `192` | Instruction/options budget within total context |
| `OMNIA_LAYA_MAX_INPUT_BYTES` | `65536` | Bounded request size including metadata |
| `OMNIA_LAYA_MIN_PROBABILITY` | `0.8` | Review threshold, selected per task using evaluation |
| `OMNIA_LAYA_DATABASE` | `var/omnia/decisions.sqlite3` | Private durable ledger path |

The model is explicit per run. Use the multilingual checkpoint for the relevant
language workload. Maximum accepted configuration is 512 tokens for English,
1024 for typed-decisions and 8192 for multilingual. Actual state capacity is lower
because instructions and options share that budget. Longer context is a budget,
not a promise of equal accuracy at every length.

Windows PowerShell, using the revision exercised in the local verification:

```powershell
$env:OMNIA_LAYA_REVISION = '55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851'
$env:OMNIA_LAYA_DEVICE = 'cpu'
python -m examples.omnia --input examples/omnia/requests.jsonl
```

Linux/macOS:

```bash
export OMNIA_LAYA_REVISION=55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851
export OMNIA_LAYA_DEVICE=cpu
python -m examples.omnia --input examples/omnia/requests.jsonl
```

Repeat the command to exercise durable replay. Use `HF_HUB_OFFLINE=1` after the
chosen checkpoint has been cached. `HF_HOME` controls the upstream model cache.
Do not pass credentials as input state, option descriptions or evidence IDs.

## Service ownership

Run a single bounded worker per ledger. Supervise the process externally, retain
the input stream for replay and monitor failed output rows. The CLI exits with 0
for completed processing, 1 for item failures and 2 for startup/configuration errors.
Keep database files on private local persistent storage, not in the public repository.

Record CPU/GPU, dependency versions, model revision and thread count for each
performance measurement. The first `inference_ms` includes lazy model loading;
later values include token checks and the local model call. Cache replay should
be measured separately; its stored inference duration belongs to the original run.

There is no HTTP listener in the OMNIA integration. If deploying the inherited
`laya-serve` API separately, configure its authentication and network boundary
according to the upstream deployment guide. The CLI environment does not configure
that separate server.
