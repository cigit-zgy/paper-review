# Figure and table evidence

Inventory EVERY main-text Figure and Table against the PDF before analysis.
Record an id, source location and panel labels independently of interpretation.
Captions detected in extracted Markdown are only a missing-object warning system;
check for unnumbered objects, lost captions and supplements yourself.

Each main object MUST contain: id, source_location, role, question, what_is_shown,
variables_axes_groups, comparison, main_observation, authors_interpretation,
supported_claim (claim IDs), evidence_strength, limitations, blog_role.
`blog_role` is `used` or `not used: <reason>`. A principal evidence object should
be used; explain omissions without omitting its structured analysis.

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
locally without granting the right to republish them: check rights before external
publication; use a clearly labelled original explanatory schematic when appropriate.
