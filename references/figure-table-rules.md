# Figure and table evidence

Inventory EVERY main-text Figure and Table against the PDF before analysis.
Record an id, source location and panel labels independently of interpretation.
Captions detected in extracted Markdown are only a missing-object warning system;
check for unnumbered objects, lost captions and supplements yourself.

Each main object MUST contain: id, source_location, role, question, what_is_shown,
variables_axes_groups, comparison, main_observation, authors_interpretation,
supported_claim (claim IDs), evidence_strength, limitations, blog_role.
`blog_role` is `used` or `not used: <reason>`. Every main object must be marked
`used` and explained in the blog; `not used` is reserved for supplementary objects
outside its argument. Rights restrictions omit reproduction, never main-object analysis.

For every multi-panel figure, store `panels: [{id: a, role: ..., relationship: ...}]`
covering ALL labels in the independent inventory. Discuss axes, units, conditions,
groups, uncertainty and statistical comparisons where applicable. For a process
diagram, identify inputs, outputs and arrows instead of inventing numeric axes.
Explain how the panels jointly support the argument, not only what each caption says.

Tables require interpretation of rows, columns, units, baselines, unavailable
values, significance markings and comparison fairness as applicable. A table
transcription or caption translation does not count as interpretation.

Supplementary objects may be brief unless a core argument or the blog uses them;
then apply the same full requirements. Record omitted/unavailable supplements
as limitations and block any essential dependent claim. Figures may be retained
locally without granting republication rights.

## Presentation and rights gate

Object inventory is independent of blog ordering. Explain all main objects in
question-driven prose under scientific H2/H3 titles; never turn object numbering
into the article directory. A joint discussion can combine objects while preserving
each object's panels, observations, supported claims and limits. The structured
review remains the exhaustive audit surface; the blog is the connected argument.

Before publishing each original figure/table, record its source URL, source PDF
page/object, asset SHA-256, license URL, attribution, third-party credit inspection,
unchanged/adapted status and use context. Inspect the actual object and its caption,
not only the article-level license. Unclear or excluded rights automatically mean
no reproduction; retain full textual explanation and record discussion_only.

CC BY-NC-ND 4.0 permits sharing unadapted licensed material in a noncommercial
context with author/source attribution and a license link. It does not authorize
sharing adapted figures. Preserve complete original content: no added annotations,
data changes, recoloring, panel recombination or near-redrawing. Prefer original
publisher asset bytes; responsive display resizing must preserve aspect ratio and
must not hide/crop content. Link the full-size asset for detailed inspection.
Check third-party credit lines for exclusions. Do not assume an article license
covers explicitly excluded third-party material. Reassess rights if use becomes
commercial or the requested object changes.

In the Chinese figcaption identify the original object, authors, paper/journal,
DOI, license and unchanged status. Write the reviewer's explanation outside the
image, with its interpretation distinguished from the source caption. A caption
translation alone is not analysis. No license checker can replace this inspection.
