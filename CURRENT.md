# Current capability

Single-paper local MinerU extraction adapter, structured scientific evidence review,
and Chinese figure/table-centred MDX draft workflow. Current semantics are maintained
in reports/design/README.md and projected by SKILL.md and references/.

The offline suite passes. Real-paper qualification is a separate step and must not
be inferred from synthetic fixtures or deterministic validation alone.

Source adjudication now binds raw extraction and original PDF hashes without
rewriting inputs. Chinese discussion-only sections and distinct Extended Data /
reporting identifiers support source-based review without reproducing images.
The offline regression suite contains 42 passing tests; scientific acceptance
requires an independent source-level review for each real paper.
