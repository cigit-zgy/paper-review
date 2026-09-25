# Narrative-first, evidence-centered academic Chinese review

Pass review-stage validation before writing. Read current target-main rules and
PAPER_REVIEW.md; record the checked commit. Preserve the structured review and
source adjudications. Scientific claims must not expand merely to improve a story.

## Argument before outline

Begin with a bounded conclusion and develop a continuous argument:
research tension → proposed solution → how it works → whether evidence supports
it → reproduction versus open problems → what was established → limits → transfer.
These are reasoning stages, not prescribed titles. H2 owns a complete narrative
stage; H3 a scientific question, method step or evidence group; H4 only a panel,
technical detail or local dispute. The layout owns H1. No body H1, H5+, skipped
levels or Figure/Table-number headings. Do not substitute eight obligatory questions
for the old figure checklist. Select titles after deciding the causal argument.

A figure remains a first-class evidence object, not a table-of-contents entry.
Place it where it advances the question; multiple objects may support one section,
and one object may be revisited. Connect sections with the unresolved question
that motivates the next step. Do not repeat the abstract or translate IMRaD.

Explain every main-text figure/table. For every used object, make clear why it is
needed, how to read it, the observation, supported claim, evidence boundary and
reviewer's judgment. These may span connected paragraphs. Do not require visible
问题/读图方法/核心观察/支持判断/证据边界 labels. Preserve panel/axis/unit/group,
comparison, uncertainty and denominator semantics. Meaning and completeness are
checked independently by a source-level reviewer, not by counting labels.

## Evidence binding without visible checklist prose

Wrap the relevant prose/figure in a plain, non-nested semantic section:

```mdx
<section data-evidence="Figure 1; Table 1" data-claims="C01 C02">

### 为什么这组比较能够检验方法

连续的中文分析，明确提到原文图1与原文表1，解释读法、观察和推断边界。
图像/表格及图注放在推进论证的位置，不用编号作标题。

</section>
```

Use exact manifest object IDs separated by semicolons, and claim IDs separated
by spaces. Multiple sections can bind the same object; together they must link
all its supported claims. Every used object needs nonempty Chinese analysis and
an explicit reader-visible reference. Unknown objects/claims fail. Bindings in
comments or code are not evidence. This is provenance metadata, not a second
scientific source or a style visible to readers. Do not nest section wrappers.

For reproduced figures use semantic figure/img/figcaption with Chinese alt and
caption; for source tables use ResponsiveTable with the caption above. Static
workspace-relative assets must exist. Admitted site paths are checked separately
in the target build. For rights-limited or deliberately omitted reproductions,
set publication.mode=discussion_only and a specific reason; full discussion remains
mandatory. See figure-table-rules.md for the rights gate. Independently compiled
facts or conceptual diagrams must be identified as reviewer synthesis.

## Language and semantic elements

Write academic Chinese: coherent paragraphs, restrained conclusions, Chinese
headings/captions/table headers. Retain necessary paper titles, journals, proper
method names, abbreviations, variables, equations and code. Introduce specialist
terms as 中文（English） when useful, then remain consistent. Typical complex
methods reviews need about 4,000–7,000 Chinese characters; evidence depth and a
continuous argument decide length, never filler or a numerical quota.

- Ordered lists: genuine steps, causal chains or decision criteria.
- Unordered lists: parallel conditions, limits or design elements.
- Blockquotes: short attributed source propositions, or an explicitly identified
  central judgment under discussion; never decorative emphasis or invented quotes.
- AcademicCallout: note/definition/method/caution with an explicit Chinese label.
- ResponsiveTable: factual comparison or synthesis, not a prose layout device.
- Mermaid: only the reviewer's independent conceptual process/logic, clearly labelled.
- Code fences: only when an interface, data structure or pseudocode is itself
  explanatory evidence. Do not force a code example to vary the page visually.

## Final prose cleanup

After the scientific draft is complete, run one whitelist-only AI-tone cleanup
using `larashero3-dotcom/lieflat-less-ai-tone` pinned at
`27d29232f10124db904ca9c0536d0b67cb3b2833` as a secondary style reference.
Apply only rules with an explicit textual trigger. Typical targets include
翻案腔, empty list-introduction colons, repeated adjacent sentence frames,
paragraph-opening comments without a referent, and abstract improvement wording
when the same paragraph already contains exact values.

This pass MUST preserve heading hierarchy, section/paragraph order, lists, tables,
quotes, code blocks, evidence bindings, factual content, numerical values,
uncertainty and claim strength. Do not add colloquial fillers, alter sentence
length merely for rhythm, or rewrite text that does not hit a listed rule.
Academic Chinese, source fidelity and this Skill's evidence contract take
precedence over the secondary style reference.

Use only needed existing components, KaTeX and styles. Add no CSS/font/theme layer.
Keep draft:true until authorized admission. Include verified paper metadata/DOI
and per-object source/license attribution. Run review/blog validation, independent
scientific review, target checks and actual desktop/mobile inspection. This Skill
itself does not grant permission to write to a blog or publish it.
