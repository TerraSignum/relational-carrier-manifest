# P0 — Reader's Guide to the Relational Carrier Theory Corpus

[![CI: reproduce](https://github.com/TerraSignum/relational-carrier-manifest/actions/workflows/reproduce.yml/badge.svg)](https://github.com/TerraSignum/relational-carrier-manifest/actions/workflows/reproduce.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is the canonical entry-point document for the
relational-carrier-theory corpus (Papers 1–6 and the bridge note).

P0 is a **synthesis**, not a paper:

- Every claim cites the load-bearing source paper.
- No new numerical result, no new derivation, no new proof is
  introduced here.
- The closure grammar (EXACT / PRECISE / FACTOR2; load-bearing /
  downstream / supporting / external / open) is defined in the
  technical papers; P0 only routes the reader.

If a statement in P0 and a statement in the cited paper disagree,
the cited paper is authoritative.

## Build

```bash
cd paper
tectonic -X compile manifest.tex
```

Produces `manifest.pdf` (~110 KiB).

## Contents

The PDF is structured as:

1. What this document is and is not
2. One-sentence thesis + one-paragraph genealogy
3. Three load-bearing claims (P2, P3, P4)
4. Two branches: vacuum and matter-side chirality flip
5. Corpus map: paper → role table
6. Claim grammar (closure tiers + claim classes)
7. Main closures at a glance (top-tier table)
8. Falsification handles (cosmological + laboratory + prospective)
9. Where to read next (routing by question)

## Relationship to other corpus documents

| Document | Role |
|---|---|
| **P0** (this) | Reader's guide / corpus map / claim grammar / falsifiers |
| **bridge note** | Lemma-level technical consistency P1 ↔ P4 |
| **P6** | Master technical document (UV carrier, action, branches, ledger) |
| **P1–P4D** | Sector-specific closure papers |

## License

Independent research project by Sandro Bucciarelli; correspondence
to `sandro.bucciarelli89@gmail.com`.