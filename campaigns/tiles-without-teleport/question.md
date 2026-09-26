# 3-SAT → Tiles without teleport moves

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

Tiles carry finite feature sets. Consecutive chosen tiles must share a currently present feature; moving deletes their common features. The goal is to remove all features, with no teleport or zero-effect moves.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

Removing teleportation tests whether local feature transitions alone create hardness in the puzzle model.

## Difficulty

A reduction must enforce movement and deletion together, without relying on forbidden jumps.

## Literature context

Hardness that relies on teleport moves does not settle the local-movement-only rules used here.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Man, These New York Times Games Are Hard! A Computational Perspective](https://drops.dagstuhl.de/storage/00lipics/lipics-vol366-fun2026/LIPIcs.FUN.2026.2/LIPIcs.FUN.2026.2.pdf): Alberti, Chierichetti, Giacchini, Muscillo, Panconesi and Tani, Man, These New York Times Games Are Hard! A Computational Perspective, FUN 2026, Section 5, Definitions 21–23 and Theorem 24, defines this model and solves the case where each pair of tiles shares at most one feature via an Euler-trail characterization. Section 6, printed p. 2:21, explicitly leaves arbitrary sharing number without teleport moves open. Theorem 4's polynomial algorithm permits forced teleports, so it does not settle this target.
- [full arXiv version](https://arxiv.org/html/2509.10846v1): The full arXiv version, Section 5, includes the Euler-trail proof. The version history listed only v1 when checked. The conference publication is the later inspected statement. A direct request for a v2 HTML page failed; no such version is asserted to exist.
- [version history](https://arxiv.org/abs/2509.10846): The full arXiv version, Section 5, includes the Euler-trail proof. The version history listed only v1 when checked. The conference publication is the later inspected statement. A direct request for a v2 HTML page failed; no such version is asserted to exist.

Fixed from board record `website/questions/tiles-without-teleport.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
