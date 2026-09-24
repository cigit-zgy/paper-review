# Chinese evidence-centred blog

MUST pass review-stage validation before blog generation. Read current target
main rules and component interfaces, then record the checked commit in the manifest.
The target's academic-content rules also reference Fenng/Tech-Doc-Style-Chinese;
use that secondary reference when relevant without overriding source fidelity.

Body prose is Chinese. Preserve English paper title, journal, proper method/model
names, variables, equations, code, DOI; introduce necessary technical terms as
中文（English）. Ordinary research articles are about 2500–4500 Chinese characters,
with extra space for genuinely complex methods/evidence. This is not a hard quota.
Do not translate the paper paragraph by paragraph or reproduce mechanical IMRaD.

Start with a concise conclusion, then the required sections from templates/blog.mdx.
The main narrative is Question → Figure/Table → How to read → Observation →
Evidence-supported conclusion → Critical assessment. Organize objects by argument,
not necessarily numerical order. Explain what transfers to the user's research
conditionally; do not assume wastewater applicability merely because the user
studies it.

For EVERY Figure/Table used in the blog, the blog MUST:

1. explicitly reference its canonical ID (Figure 1, Table 1, etc.);
2. supply a Chinese explanatory caption (figcaption, or a table caption ABOVE table);
3. explain the question the object answers;
4. tell readers how to read axes, groups, panels or columns;
5. identify the core observation;
6. link it to existing claim IDs;
7. explain the evidence boundary;
8. go beyond translating the original caption.

Use `## Figure 1：<scientific question>` (or Table) for the object block. To make
the writing contract checkable while retaining paragraph prose, use the labels
`问题：`, `读图方法：` (or `读表方法：`), `核心观察：`, `支持判断：`, `证据边界：`.
Each label introduces real analysis; generic filler does not meet the scientific
contract even when a structural checker passes. Cite every object's supported
claim IDs in its 支持判断 paragraph. Discuss panels individually and together.

Use semantic `<figure><img .../><figcaption>...</figcaption></figure>`, meaningful
Chinese alt text and a workspace-relative source asset. Use `<ResponsiveTable>`
around overflow-prone tables and put a Chinese caption paragraph immediately
before it. Start headings at h2: the site supplies h1. Use KaTeX, language-labelled
code fences, and existing styling; no CSS, font rules or theme hex values here.
Import only components used. Optional Mermaid:
`<MermaidDiagram code={'flowchart LR\n A[输入] --> B[结果]'} alt="流程说明">`
with a caption slot; this is an explanatory schematic, never substitute evidence.
AcademicCallout uses kind note/definition/method/caution and optional label.

Use `draft: true`. Keep a references section identifying the reviewed paper using
verified bibliographic metadata and DOI if reported. Do not add placeholder or
unread citations. Before blog publication, move/copy assets to the destination's
article asset location, rebase paths, check image rights, run that repository's
Astro/lint/format/build checks, and inspect desktop/mobile rendering. This Skill
generates a draft package; it does not authorize a blog-repository write or publish.
