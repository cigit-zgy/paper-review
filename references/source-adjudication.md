# Source-PDF adjudication

Extraction is a reading aid; a legible original PDF is the authority. Never
overwrite raw Markdown/JSON to hide parser defects. Missing source evidence is
not repairable by inference. Scope missing supplements explicitly and omit any
conclusion whose required evidence is unavailable.

When visual inspection can settle an extraction discrepancy, add an optional
top-level `adjudications` list to the manifest. Each record requires:

- `id`: A01, A02, etc.; `status`: verified or unresolved.
- `source_page`: physical one-based PDF page; `source_object`: a registered object
  ID, or Document for non-object metadata.
- `pdf_sha256`: source PDF hash; `raw_file`: workspace-relative raw file path;
  `raw_sha256`: that file's hash; `raw_locator`: line or JSON page/block location.
- `raw_observation`: what the extraction says or loses.
- `pdf_observation`: precisely what was visually verified, with exact transcription
  when a claim needs a source quotation; distinguish transcription from description.
- `interpretation`: adjudicated meaning; `limitation`: remaining uncertainty or
  scope; `verified_by`: the actual inspecting actor, never an invented reviewer.

Keep the discrepancy in review.uncertainties. An originally blocking discrepancy
may retain `blocks_blog: true` and add `resolved_by: A01`; the referenced verified
record resolves that specific discrepancy. Unlinked or unresolved blockers still
fail. All registered unresolved adjudications fail; keep unrelated, omitted-scope
limits in nonblocking uncertainties instead of claiming they were resolved.

A claim may use `evidence_adjudication: A01`. Its evidence_text must then match the
record's PDF observation and its source page/object must agree, instead of matching
the damaged raw Markdown. Label visual descriptions as reviewer observations, not
verbatim author text. Unaffected claims continue to cite raw source excerpts.

The validator checks hashes, nonempty fields, status and links. It does not prove
that the actor looked at the PDF, that a page number is correct, or that an
interpretation is scientifically justified. Independent source review remains
required. Recreate the private workspace from the same source to rerun validation;
never publish the PDF merely to make an evidence package self-contained.

Use distinct `Extended Data Figure N` / `Extended Data Table N` IDs for publisher
extended data, keeping Supplementary `Figure SN` IDs distinct. `Reporting Table N`
is an internal inventory ID for an unnumbered reporting form; explicitly state
that this number was assigned for review, not printed in the original paper.
