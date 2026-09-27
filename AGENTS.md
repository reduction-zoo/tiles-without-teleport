# Research instructions

Read the [fixed question](campaigns/tiles-without-teleport/question.md), [prior state](campaigns/tiles-without-teleport/state.md) and [preparation notes](campaigns/tiles-without-teleport/work/preparation.md). The fixed [test corpus](campaigns/tiles-without-teleport/work/cases.json) and [verifier](campaigns/tiles-without-teleport/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/tiles-without-teleport/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
