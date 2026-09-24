# paper-review

Read one scientific PDF in full, construct a source-linked scientific review,
and write a narrative-first Chinese blog grounded in Figure/Table evidence. The Skill guides
an agent's reading and reasoning. Its scripts manage files and check structure;
they do not generate scientific conclusions.

## What this skill does

- Reuses an existing local MinerU installation for full-document extraction.
- Separates author claims, observed evidence, interpretation and critical assessment.
- Requires an inventory and interpretation of every main-text Figure and Table,
  including individual panels and their logical relationships.
- Produces a structured review, a small YAML manifest and a Chinese MDX draft.
- Blocks blog generation when essential evidence analysis is incomplete.

## What this skill does not do

This is not a literature/systematic review system, research agent, citation search
engine, PDF summarizer, or referee-report generator. It has no RAG server, vector
database, backend, model API or plugin framework. It does not autonomously publish
articles, establish scientific truth, or grant permission to reproduce paper figures.

## Architecture

```text
scientific PDF → existing local MinerU → Markdown + figures/tables/assets
  → agent reads full paper → structured paper-review.md + manifest.yaml
  → review gate → Chinese evidence-centred blog.mdx → blog gate → human review
```

`SKILL.md` routes to four focused references. `schemas/` defines the manifest.
`templates/` supplies unfinished scaffolds. Three scripts implement initialization,
extraction glue and deterministic validation. `tests/` contains offline synthetic
fixtures and a direct unittest runner. `reports/design/README.md` owns maintained
semantics. Local task/execution records are not part of this public distribution.

## Requirements

- Python 3.12+ and uv; dependencies are PyYAML and jsonschema, locked by uv.lock.
- An existing local MinerU installation. This adapter was inspected and probed
  with MinerU 4.0.2 / Python 3.12.13. Do not install a second parser environment.
- An agent or human capable of reading the entire source, inspecting figures,
  and making explicitly qualified scientific assessments.
- Access to the current writing rules of the target blog before generating MDX.

From this Skill directory, run `uv sync --locked`. Scripts may also be run directly
with a Python environment containing the two dependencies. No global tooling
installation, Conda migration, pytest or Python package scaffold is required.

## MinerU integration

Locate the existing `mineru-kit` and its sibling `mineru`. Inspect their help/version;
the wrapper supports the verified 4.x local batch interface, with a capability probe:

```sh
uv run python scripts/extract_pdf.py --probe --mineru-kit "/existing environment/bin/mineru-kit"
```

Pass `--mineru-kit` or set `MINERU_KIT` to the existing executable. Paths containing
spaces are supported. The wrapper uses a subprocess argument list, not a shell.
It runs local batch parsing with `--pages all --format zip --tier standard` so images
are exported together with Markdown. Plain Markdown export alone may omit asset
materialization; the inspected MinerU ZIP exporter preserves it. `basic` and
`advanced` can be explicitly selected; `flash` is never the reading default.
It passes neither `--remote` nor a remote URL and does not change service/model
configuration. The existing local models still must be usable on the host.

When another version/interface is present, inspect that version's authoritative
export contract, then provide its complete local export:

```sh
uv run python scripts/extract_pdf.py "/reviews/paper one" --from-extracted "/existing export/paper.md"
```

The importer preserves relative asset paths, normalizes the main Markdown name
to `paper.md`, rejects missing assets/symlinks and refuses existing output. It is
an import adapter, not a PDF parser. It cannot prove extraction completeness or
that a manually supplied export came from the intended PDF; inspect both.

## Quick start

Run from the Skill directory. The review workspace must be OUTSIDE this source tree.

```sh
uv run python scripts/init_review.py "/papers/paper one.pdf" "/reviews/paper one"
uv run python scripts/extract_pdf.py "/reviews/paper one" --mineru-kit "/existing environment/bin/mineru-kit"
```

Then ask the agent to follow `SKILL.md`: read the entire paper and relevant
supplements, visually inspect the evidence, populate the independent inventory,
and complete `review/manifest.yaml` plus `review/paper-review.md`.

```sh
uv run python scripts/validate_review.py "/reviews/paper one" --stage review
```

Only after this gate passes and the current blog rules are read, copy
`templates/blog.mdx` into the workspace's `output/blog.mdx` and write the article.
Replace the sample metadata/date, adapt the narrative and hidden evidence bindings to the actual paper,
remove unused component imports and keep `draft: true`.

```sh
uv run python scripts/validate_review.py "/reviews/paper one" --stage blog
```

`PASS` means deterministic checks passed. A nonzero exit means the named evidence
or artifact defect must be addressed; never use it to silently discard a figure.

## Output structure

```text
review-dir/
├── source/paper.pdf
├── extracted/
│   ├── paper.md
│   └── assets/          # or images/, as emitted by the installed MinerU
├── review/
│   ├── manifest.yaml
│   └── paper-review.md
└── output/blog.mdx     # created only after the review gate
```

Do not commit this workspace to the Skill repository. Deliver needed assets with
the MDX; local links are relative to their document. `init_review.py` refuses
existing destinations and does not create a premature blog draft.

## Evidence model

See [evidence rules](references/evidence-rules.md),
[review contract](references/review-contract.md) and the
[manifest schema](schemas/paper-review.schema.json). A claim contains:

```yaml
id: C01
author_claim: "Author assertion, verified against the paper"
source_section: Results
source_page: 8
figure: [Figure 3b]
evidence_text: "A short exact source excerpt"
interpretation: "Explicitly attributed reading of the evidence"
critical_assessment: "Inference strength and its conditions"
```

This is a structural example, not evidence from a real paper. Real entries require
actual source text. Excerpts are whitespace-normalized and checked against the
extraction; this does not prove their scientific relevance. Innovation blocks
resolve claim IDs or explicitly say `not established`.

## Narrative-first, evidence-centered writing

Every main object needs analysis in both the review and final blog. Core
supplementary evidence receives the same treatment. Omitted non-core supplements
need a documented reason.
For each used object, write a Chinese caption, question, reading guidance,
observation, supported claim and evidence boundary. Explain panel relationships;
do not merely translate captions. Scientific questions determine headings, not
figure numbers. Use hidden section evidence/claim bindings; visible five-label
checklists and fixed section titles are no longer required. Every original image
must pass the per-object rights gate. See [figure/table rules](references/figure-table-rules.md)
and [blog writing](references/blog-writing.md).

Complex method reviews usually need about 4,000–7,000 Chinese characters;
continuous argument and complete evidence determine depth. This is guidance, not a word-count test. English paper titles,
journal names, proper names, symbols, code and DOI stay in their original form.

## Integration with water-modeling-notes

Target: [cigit-zgy/water-modeling-notes](https://github.com/cigit-zgy/water-modeling-notes).
The initial contract was checked at main commit
`e0251db18838324e329943502d20b40555b8e9e2`. Re-read current main on EVERY use:
AGENTS.md, academic-blog SKILL.md and academic-content.md, content schema and used
component interfaces. A checkout can lag remote main; record the inspected SHA.

The template uses supported frontmatter, H2–H4 narrative sections, `ResponsiveTable` and
`AcademicCallout`. Optional diagrams use `MermaidDiagram` with `code`, `alt` and
caption slot; no CSS/components are copied. Keep the site's centralized typography,
Dracula theme, regular body weight and Chinese font handling. Tables have Chinese
captions above them; figures have alt text and explanatory captions.

Publication is a separate authorized step: choose a stable descriptive MDX filename
in the target's current Paper Review collection, copy cleared assets and rebase links, run the target project's
`pnpm astro check`, `pnpm lint`, `pnpm format:check`, `pnpm build`, and inspect
desktop/mobile rendering. Drafts must stay out of routes, lists, RSS, sitemap and
Pagefind. The Skill creation task does not modify the blog's actual content.

## Design references

All six are **REFERENCE_ONLY** for design, not copied code or installed project
dependencies. The separately installed MinerU parser is called as the requested
local tool. This project is not a fork of any of them.

| Project | Principle referenced | Not adopted |
| --- | --- | --- |
| [OpenDataLab/MinerU](https://github.com/OpenDataLab/MinerU) | Structured document extraction and asset-preserving export | Parser reimplementation, bundled models or forced remote service |
| [MinerU-Document-Explorer](https://github.com/OpenDataLab/MinerU-Document-Explorer) | Navigable deep reading and element-level evidence | Knowledge index, wiki ingestion, MCP/search infrastructure |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | Traceable document context for claims | RAG search, LLM orchestration and citation database |
| [AkariAsai/OpenScholar](https://github.com/AkariAsai/OpenScholar) | Claims grounded in identifiable scientific passages | Retrieval/reranking corpus, training and multi-paper synthesis |
| [stanford-oval/storm](https://github.com/stanford-oval/storm) | Structured evidence-informed long-form composition | Topic research, web retrieval and persona generation |
| [sodalone/paper-reading-skill](https://github.com/sodalone/paper-reading-skill) | Single-paper decomposition and claim/evidence assessment | arXiv-specific acquisition, external literature pipeline and referee framing |

## Limitations

- PDF inventory, reading coverage and source metadata depend on truthful human/agent
  inspection. Caption recognition is a backstop and may miss unusual layouts.
- Deterministic checks cannot judge scientific validity, real novelty, excerpt
  relevance, Chinese prose quality, exact visual correspondence or image rights.
- The blog checker supports the documented static MDX pattern, not arbitrary JSX.
  Dynamic image expressions require a separately verified destination workflow.
- Synthetic tests do not establish MinerU model accuracy or real-paper review quality.
- Missing formulas/tables/images must be recorded as uncertainty; unresolved
  essential defects block dependent prose. No silent hallucination or parser fallback.

## Development/testing

```sh
uv sync --locked
uv run python tests/run_tests.py
uv run python scripts/validate_review.py --help
```

Tests run offline after dependencies are installed. They generate only a labelled
PDF presence stub, never run a large MinerU model, and exercise an entire synthetic
flow using a fake CLI subprocess. Fixtures are explicitly synthetic and contain
no real-paper text. Review the documented scientific behavior separately from
test counts. MIT applies to this Skill, not to users' PDFs or extracted figures.
