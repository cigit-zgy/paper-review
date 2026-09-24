# Evidence and provenance

Keep claim/object links reciprocal: an object's supported_claim IDs must list that
object in each claim's figure array, and conversely. Panel references resolve to
their parent object for this check. Review and blog prose may cite only registered
claim/object IDs; these identity checks do not assess scientific relevance.

The supplied PDF and its checked MinerU extraction own paper facts. Do not fill
missing paper-specific facts using field knowledge, abstracts, titles, web summaries
or another paper. Preserve negative results, contradictory observations and author
limitations. Outside context, if explicitly requested, must be labelled and cited
separately; it does not replace this paper's evidence.

For each claim record `id`, `author_claim`, `source_section`, `source_page`,
`figure` (an array of Figure/Table IDs, possibly empty), a short verbatim
`evidence_text`, `interpretation`, `critical_assessment`. A supporting object may
include a panel reference such as Figure 3b, whose parent and panel must exist.
Use concise source excerpts; preserve original language, quantities and units.
When an excerpt cannot be matched to Markdown because OCR/formatting is damaged,
repair it using the original PDF and mark the extraction issue rather than inventing
a quote. The deterministic checker normalizes whitespace, not scientific meaning.

Four layers must remain explicit:

1. Author claim: what the authors assert.
2. Evidence shown by the paper: actual observation, comparison, proof or protocol.
3. LLM interpretation: an explicitly attributed explanation of its meaning.
4. Critical assessment: inference strength, alternative explanations and limits.

Do not recast layers 3–4 as author conclusions. Source-page locators are positive
PDF page numbers; printed page labels can be added in source_location. Record
section and page even for claims without a figure. Source facts must never be
replaced by synthetic values. Synthetic examples belong only in labelled tests.

If MinerU loses equations, table headers, units, image panels, or reading order,
inspect the original region. Record uncertainty and stop dependent conclusions
when unresolved. Do not silently select a lower-quality tier or remote upload.
MinerU success alone does not prove complete or accurate extraction.
