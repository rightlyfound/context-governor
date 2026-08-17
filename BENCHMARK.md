# Benchmark Methodology

The benchmark is designed to study whether structured context anchoring can reduce wasted context and interaction overhead in repository debugging. It is not a claim that any provider is universally superior.

## Method

Each task is evaluated in vanilla and ACG-wrapped modes using the same repository snapshot, question, model, and stopping criteria. Logs are written to `showcase_logs/`. Provider usage metadata is preferred for token counts; offline mode reports deterministic proxy values and labels them accordingly.

The methodology is informed by long-context research, including the observation that relevant information can be underused when placed in the middle of a long context. See the [Lost in the Middle paper](https://arxiv.org/abs/2307.03172) and related retrieval-augmented generation literature.

## Metrics

Token Economy is total input and output tokens across turns. Round-Trip Efficiency is the number of user-assistant exchanges. Precision is the proportion of expected corrected lines matched by the submitted solution. Every result must include raw logs and the exact repository snapshot used.

## Compare with industry approaches

ACG is a context-selection and anchoring protocol, whereas RAG systems retrieve external documents. The approaches are complementary: RAG can supply candidate context, while ACG can request missing local anchors and preserve structural continuity. No comparative score is published unless it has been measured using the same tasks and settings.
