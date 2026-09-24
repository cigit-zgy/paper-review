# Paper review design

This file owns the maintained capability design.

## Boundaries and flow

One local scientific PDF → existing local MinerU → complete Markdown/assets →
agent-authored scientific review and evidence manifest → Chinese evidence-driven
MDX → deterministic validation. No model API, retrieval service, PDF parser,
database, backend, or multi-agent framework is added. All six requested external
projects are REFERENCE_ONLY; the installed MinerU executable is reused as a tool.

The three Python scripts initialize a new external workspace, export/import a
MinerU bundle, and validate artifacts. Use Python 3.12, uv, PyYAML and jsonschema;
do not create a Python package hierarchy. Tests use unittest, never pytest.

## Evidence and gates

The manifest is the machine-readable index; paper-review.md remains the core
scientific narrative. A reader inventories every main-text Figure/Table against
the PDF independently of analysis, including panel labels, and records full-text
coverage. The validator compares this inventory with registered interpretations
and extracted caption candidates. Automated caption detection is a backstop, not
proof of PDF completeness. The inventory and coverage attestations require actual
source inspection by the agent or human.

Every evidence object separates observations, author interpretations, supported
claims, limitations and blog use. Claims include source section/page and a short
verbatim evidence excerpt, with interpretation and critical assessment separate.
Innovation blocks require resolvable claim IDs or literal `not established`.
Supplementary objects cited in core arguments receive the same full analysis.

`validate_review.py --stage review` is required BEFORE copying the blog template
or authoring blog prose. It checks full review coverage, object/panel completeness,
claim links and local paths. `--stage blog` additionally checks MDX frontmatter,
required Chinese sections, object references, captions, asset paths and structured
evidence discussion. Neither gate certifies scientific truth or publication rights.
Missing evidence fails closed; interpretation uncertainty is explicit. Templates
are unfinished drafts and intentionally cannot pass a finished-artifact gate.

## Blog integration

Consult current target-main rules on every use. Initial interface baseline:
water-modeling-notes main e0251db18838324e329943502d20b40555b8e9e2.
Use h2 sections, valid four-topic frontmatter, draft=true, semantic figures with
Chinese captions and alt text, captions above ResponsiveTable, and optional
MermaidDiagram(code, alt) / AcademicCallout(kind, label). Reuse target styling;
do not copy its components/CSS. The blog proceeds by questions and evidence,
not the paper's IMRaD structure. Suggested 2500–4500 Chinese characters is guidance.

## Publication

This repository publishes the Skill source under MIT. Source PDFs, extracted
real-paper content, caches and local execution records stay outside the repository.
Synthetic fixtures are explicitly labelled and contain no real research findings.
User authorization and source-image reuse rights are required before publishing
any article generated with this Skill.

## Source adjudication

Original-PDF observations may resolve extraction defects only through explicit,
SHA-256-bound records. Preserve raw files; record source page/object, raw locator
and observation, visual observation, interpretation, limitation and reviewer.
Only linked verified records resolve a blocking uncertainty. Adjudicated claim
excerpts must belong to the matching observation, page and object.
See references/source-adjudication.md.

Extended Data figures/tables and internally numbered reporting tables have distinct
IDs. Chinese discussion-only evidence sections preserve all scientific analysis
without reproducing source images. Missing supplements limit dependent claims.
Independent scientific review and publication authorization remain separate gates.

## Validation boundary

Offline tests cover success and rejection cases, paths with spaces, missing
source/interpretations, panels, malformed/duplicate YAML, invalid links and
MinerU glue without models. Test the real installed CLI capability probe; a real
PDF/model parse and scientific review quality are outside the synthetic test claim.
MDX compilation and target frontmatter checks establish interface compatibility;
they do not substitute for native page/layout acceptance of a future real article.
