# Structured scientific review

Use `templates/paper-review.md`. Every required top-level section must contain
substantive source-grounded analysis. Use explicit “not reported” with a reason
when the paper lacks information; do not fabricate an experiment for a theory paper.

Required sections: Paper identity; One-sentence contribution; Research question;
Scientific motivation; Method architecture; Data and experimental design; Main
findings; Claimed innovations; Figures and tables; Limitations; Reproducibility;
Transferability; Critical assessment.

Each `## Innovation N` contains Author claim, Prior approach / comparison target,
What actually changed, Supporting evidence, Reviewer assessment, Transferability.
Supporting evidence lists manifest claim IDs (e.g. C01), or says `not established`
and explains why. Neither a new acronym nor a reported improvement establishes
novelty. Distinguish reported baselines from unexamined literature; no search engine
or external literature corpus is part of this Skill.

`paper-review.md` is the core scientific narrative. The manifest indexes the
evidence and stores the full Figure/Table records without duplicating them in
another database. In the narrative, discuss every analysed object by its canonical
ID and explain its contribution to the argument; a link-only object list is not enough.

## Manifest editing

Follow `schemas/paper-review.schema.json` and the annotated manifest template.
All paths are relative to the workspace, not the Skill or current shell directory.
Paper metadata can explicitly say “not reported”; dates/year use null when unknown.
Missing DOI is not permission to invent one.

Inventory fields identify the objects visible in the original PDF independently
of completed interpretations. `inventory_checked: true` means the reader checked
main text and relevant supplement against the PDF, not just regex matches.
`full_text_read: true` and `coverage` record which sections/pages were read.
These are attestations; the validator cannot establish their truth.

Objects include `scope: main|supplementary`, `core_argument: true|false`, and
panel records for every panel label in inventory. Main objects and supplementary
objects used in a core argument require all analytical fields. A non-core
supplement may use only identity/location/role, a brief observation and blog role.
If it is used in the blog, promote it to full analysis first.

Set `review.status: reviewed` only after actual reading and analysis. Extraction
issues carry a location, description and `blocks_blog`; unresolved essential
formula/table/image defects MUST use true. Normal scientific uncertainty belongs
in the scientific interpretation and evidence-strength fields, not in invented data.
