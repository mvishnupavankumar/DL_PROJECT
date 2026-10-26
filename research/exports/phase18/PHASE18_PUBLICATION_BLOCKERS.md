# Phase 18 Prioritized Publication Blockers

**Current release verdict:** **BLOCKED**

| Priority | Blocker | Why it blocks publication | Required action | Accountable role |
| ---: | --- | --- | --- | --- |
| 1 | No reproducible DOCX/PDF generation toolchain | The Markdown source cannot yet produce the required review/release formats through an approved installed method. | Provide an approved installed renderer and document exact versioned commands. | Environment owner |
| 2 | No page-by-page visual inspection | No PDF exists and no page rasterizer is available; layout, figures, equations, references, margins, and glyphs are unverified. | Render final PDF, rasterize every page, inspect every page, and record defects/corrections. | Research engineer/reviewer |
| 3 | Release provenance not frozen | The active worktree is dirty; existing historical manifests must not be recast as a current clean release. | Select release inputs, record hashes and Git state, then create a new scoped manifest without modifying historical manifests. | Release manager |
| 4 | Author and venue metadata unconfirmed | Author, affiliation, corresponding-author, date, venue, and template cannot be invented. | Manuscript owner supplies and approves complete metadata/template requirements. | Manuscript owner |
| 5 | AnoMod publisher-page verification/limitation unresolved | Bibliographic release status remains conditional; archive provenance does not establish external evaluation. | Confirm publisher metadata or retain an explicit accepted limitation. | Manuscript owner/supervisor |
| 6 | Source-to-render figure/table/reference verification incomplete | Source mappings are documented, but visual wrapping and rendered cross-references are not inspected. | Complete REL-05 during the rendered-document review. | Research engineer/reviewer |
| 7 | Final independent release decision pending | A source-level audit cannot self-authorize publication. | Designated supervisor/release manager reviews completed checklist and issues the final decision. | Research supervisor/release manager |

Non-blocking but mandatory evidence boundaries remain: live LSTM detection performance is **UNMEASURED**; Experiment A is synthetic, Experiment B is a six-case exploratory pilot, Experiment C is a bounded local safety harness, and Experiment D remains unexecuted/excluded from confirmatory claims.
