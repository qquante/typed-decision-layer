# Research foundations

Research informs a concrete engineering choice here. Citations do not transfer a
paper's benchmark results to this repository or imply endorsement by its authors.

| Reference | Relevance | Application in this fork |
| --- | --- | --- |
| [Laya source and documentation](https://github.com/NandhaKishorM/laya) | Local typed decisions, checkpoint routing, inference and calibration interfaces | Preserve the runtime; add bounded input handling and an evidence ledger around it |
| [TypeSafe Jev documentation](https://docs.typesafe.ai/) | Typed machine decisions and explicit workflow control | Keep decisions separate from application actions; document the protocol lineage without claiming shared weights |
| [Deng et al., Jev for Scientific Decisions, 2026](https://arxiv.org/abs/2609.24965v2) | Evaluates relational choices and downstream quantities separately; arithmetic belongs in code | Store individual question results and evidence so a final status cannot hide an incorrect intermediate choice |
| [Warner et al., ModernBERT, 2024](https://arxiv.org/abs/2412.13663) | Encoder architecture underlying Laya's English checkpoints | Use the actual checkpoint's token budget, pinned revision and local runtime; do not infer limits solely from the base encoder |
| [Guo et al., On Calibration of Modern Neural Networks, 2017](https://arxiv.org/abs/1706.04599) | Confidence calibration and temperature scaling | Evaluate probability calibration with ECE; retain probability and entropy-based confidence as separate fields |
| [Geifman and El-Yaniv, SelectiveNet, 2019](https://arxiv.org/abs/1901.09192) | Selective prediction and the risk/coverage trade-off | Report coverage and error among accepted decisions; our threshold gate is not an implementation of SelectiveNet training |
| [Gebru et al., Datasheets for Datasets, 2021](https://arxiv.org/abs/1803.09010) | Dataset purpose, provenance, composition and intended use | Require source, labeling policy, language, split and permitted use in domain evaluation records |

## Evaluation practice

Use a reviewed, task-specific holdout separate from examples used to choose
instructions or thresholds. Report class balance, source families, language,
missing-context cases and label disagreements. Split by source/thread where
near-duplicate records could otherwise leak across datasets.

For choice decisions, the included evaluator computes accuracy, multiclass Brier
score (sum over classes, averaged across rows), negative log-likelihood, equal-width
ECE, coverage and error among accepted decisions. Zero accepted decisions returns
an undefined selective error, not zero error. Duplicate evaluation IDs are rejected.

The initial record format is:

```json
{"id":"reviewed-item-id","expected":"label","probabilities":{"label":0.8,"other":0.2}}
```

Run against your reviewed rows:

```bash
python -m examples.omnia.evaluate --input reviewed-decisions.jsonl --threshold 0.8
```

Scores across ordered levels and binary probabilities require task-appropriate
labels. Do not use choice accuracy as a universal measure of score quality. Do not
interpret model confidence as a probability of a financial outcome.

## Attribution

OMNIA Laya is an independent OMNIA EYE integration fork of Laya, maintained from
Convai Innovations' upstream source. TypeSafe's Jev is a separately developed
system. Interface concepts and cited research do not imply shared model weights,
training data, vendor affiliation or author endorsement.
