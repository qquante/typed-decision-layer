# Decision architecture

OMNIA Laya adds a local decision ledger around the upstream Laya runtime. The
integration lives in `examples/omnia/`; the upstream Python API stays intact.

```text
Evidence packet -> bounded contract -> identity + cache
                                           |
                               pinned local checkpoint
                                           |
                             complete-input preflight
                                           |
                                typed answer validation
                                           |
                              probability policy gate
                                           |
                                SQLite decision record
```

## A complete record

Each record stores source and evidence identifiers, an input hash, an ordered
question-schema hash, checkpoint revision, runtime and integration source hashes,
inference settings, answer distributions, review reasons, timestamp and duration.
Raw input text and question descriptions are not stored in the ledger. Identifiers
and output labels are retained: use application-owned opaque identifiers and keep
the database private. A hash alone is not anonymization of low-entropy content.

Cache identity includes the complete request, question/option order, engine
manifest and policy threshold. A changed checkpoint, criterion, evidence reference,
content, policy or integration implementation cannot reuse an older decision.
Cache hits return the original record and timestamp with `cache_hit=true`.

## Typed decisions

| Type | Validated result | Gate input |
| --- | --- | --- |
| `choice` | Selected label and matching probability distribution | Largest class probability |
| `noul` | Probability of the affirmative answer | Larger of affirmative/negative probability |
| `score` | Expected ordinal score and level distribution | Largest level probability |

`model_confidence` preserves upstream confidence separately. For choice and score,
that field may measure normalized entropy. It must not be silently substituted for
the probability used by the policy. A high gate value means the model favors an
answer; task-level calibration must be measured on reviewed data.

Every question must pass the configured threshold for the record to be `accepted`.
Otherwise the record is `review`, with the exact question IDs. Acceptance validates
the configured model-policy contract; it is not an authorization to publish content,
trade or make an external call. Those actions belong to product-owned services.

## Complete inputs

The integration checks UTF-8 byte size, question count and criteria count before
inference. Using the actual checkpoint tokenizer, it checks the instruction,
each criterion and full state against Laya's separate token budgets. Oversized
inputs produce a failure instead of silently truncating the content.

Checkpoint temperature corrections are checked per active question bucket.
Questions using a corrected bucket are rejected for review. An unrelated bucket's
warning does not reject a valid request. This check does not replace measuring
calibration on the application dataset.

## Persistence and recovery

The ledger uses SQLite WAL and a write transaction across inference. It permits
one active inference per database and serializes duplicate requests across
processes. Busy callers receive a bounded database error after the timeout.
Separate ledgers are independent and do not provide distributed deduplication.

A successful decision is committed atomically. Failed inference is rolled back,
then the failure class and request fingerprint are recorded. Failure records omit
exception text and are not cached as answers. Replaying the input retries the job.
A crash before commit can repeat inference; it cannot create two records for the
same key. There are no external side effects in this integration.

The JSONL command emits one result for each nonempty input line, including malformed
and oversized lines, and returns nonzero if any line fails. Review is a completed
decision. The ledger is an audit/cache store, not a background queue scheduler.

## Product boundary

OMNIA News and OMNIA Trading can consume the same envelope and supply their own
question sets and policies. This fork establishes that shared layer. It neither
imports private production stores nor includes order signing or delivery code.

See [operations](OPERATIONS.md), [validation](VALIDATION.md), and
[research](RESEARCH.md) for reproducibility and design references.
