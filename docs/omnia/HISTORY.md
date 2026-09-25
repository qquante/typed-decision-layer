# OMNIA integration history

The OMNIA contribution is organized into retrospective company milestones on
21, 22, 23, 24 and 25 September 2026. Git author dates label those work milestones.
Git committer timestamps retain when each commit was actually created. Every
OMNIA commit includes a `Retrospective-Work-Date` trailer. A milestone date does
not assert that code was written, published or deployed on that date.

The integration was assembled on 25 September 2026 against Laya upstream
`4066d5d5fbf08b66c6757ddeedbd797bd7655bc0`. Original upstream authorship, commit
history and Apache-2.0 licensing are preserved.

The review sequence separates contracts, persistence, local inference, evaluation,
documentation and publication. It uses substantive code and documentation changes;
there are no empty commits or additional model-performance claims.

## Reviewable commit sequence

This sequence replaces the initial three OMNIA commits from the same delivery.
The implementation, tests, examples and verification measurements are unchanged.
Only this history document changes in the final source tree. Commits are split
by responsibility so contracts, inference, evaluation and documentation can be
reviewed independently.

| Author work date | Commits | Scope |
| --- | ---: | --- |
| 21 September | 1 | Provenance and work milestones |
| 22 September | 6 | Contracts, answer validation, ledger, tests and architecture |
| 23 September | 6 | Settings, pinned inference, JSONL, configuration, examples and tests |
| 24 September | 6 | Evaluation, metric tests, operations, research and validation |
| 25 September | 5 | CI, attribution, artwork, README and publication history |
| **Total** | **24** | **Substantive OMNIA changes above the preserved upstream** |

| Sequence | Work date | Change |
| --- | --- | --- |
| 01 | 2026-09-21 | `docs(omnia): define integration provenance and work milestones` |
| 02 | 2026-09-22 | `feat(omnia): add bounded values and canonical fingerprints` |
| 03 | 2026-09-22 | `feat(omnia): validate evidence and typed question contracts` |
| 04 | 2026-09-22 | `feat(omnia): validate distributions and typed model answers` |
| 05 | 2026-09-22 | `feat(omnia): persist decisions with probability gates and replay` |
| 06 | 2026-09-22 | `test(omnia): cover ledger identity recovery and concurrent replay` |
| 07 | 2026-09-22 | `docs(omnia): describe decision records and persistence boundaries` |
| 08 | 2026-09-23 | `feat(omnia): require immutable local checkpoint configuration` |
| 09 | 2026-09-23 | `feat(omnia): add traced local inference and complete-input safeguards` |
| 10 | 2026-09-23 | `feat(omnia): process bounded JSONL with per-record outcomes` |
| 11 | 2026-09-23 | `chore(omnia): document runtime environment and ignore local tooling` |
| 12 | 2026-09-23 | `docs(omnia): add executable typed decision requests` |
| 13 | 2026-09-23 | `test(omnia): cover checkpoint budgets configuration and stream recovery` |
| 14 | 2026-09-24 | `feat(omnia): measure choice accuracy calibration and selective risk` |
| 15 | 2026-09-24 | `feat(omnia): expose reviewed decision evaluation through JSONL CLI` |
| 16 | 2026-09-24 | `test(omnia): verify evaluation formulas and invalid label handling` |
| 17 | 2026-09-24 | `docs(omnia): document local runtime configuration and ownership` |
| 18 | 2026-09-24 | `docs(omnia): connect engineering decisions to primary research` |
| 19 | 2026-09-24 | `docs(omnia): record contract checks and measured local inference` |
| 20 | 2026-09-25 | `ci(omnia): check contracts across Python versions and build docs` |
| 21 | 2026-09-25 | `docs(omnia): preserve upstream guide and document Apache attribution` |
| 22 | 2026-09-25 | `chore(brand): add OMNIA EYE repository artwork` |
| 23 | 2026-09-25 | `docs(omnia): publish integration overview architecture and quickstart` |
| 24 | 2026-09-25 | `docs(omnia): record the reviewed 24-commit publication sequence` |


## Verification and provenance

The original three-commit tip was
`92a3ec03bfa3b28cc30218231b0b82319c098bcd`; its source tree remains the comparison
baseline for this reorganization. The recorded inference receipt retains its
actual verification timestamp, independent of retrospective commit author dates.
Reorganization does not represent additional model training or earlier deployment.

The repository commit list and the GitHub profile contribution calendar are
different views. GitHub's [profile contribution criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)
exclude commits made only in forks from the profile calendar. This repository
keeps its genuine fork relationship and original upstream history.
