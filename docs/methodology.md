# GrokBots: The Hidden Cost Experiments
## Methodology, data & reproducibility

**Allegorise | Version 1.0 | Experiments: 24 November 2026**

### 1. Research objectives

This exploratory case study investigates the usage overhead of operating a personal team of AI agents in Grok Bot. It asks whether batching, context reuse, reduced delegation, selective data retrieval, concise reporting and deterministic automation can reduce the token usage and estimated monetary cost of completing everyday work.

This is an account-level observational experiment, not a randomized benchmark or an official xAI pricing study. Results describe the tested environment and should not be generalized to all accounts or models.

### 2. Experimental environment

The production team consisted of seven specialized agents (project management, finance, marketing, development, administration, analysis and design). An additional test agent, TokenLab, was created during the study. Tests were initiated through Grok Bot and usage was recorded through the Grok usage dashboard CSV exports. The export does not identify individual bots or the underlying model for Grok Bot events. Agent identity was established from the experiment log and screenshots, not the billing rows. The account's precise model routing and cache expiry settings were not independently observable.

All recorded experiment times below are UTC on 24 November 2026 (Prague local time was UTC+1). Production routines were paused partway through the experiment to reduce interference; some unsolicited activity still occurred. No claim is made that the agent's internal execution state was fully controlled.

### 3. Data collection and event attribution

Three exports were available: a 500-row historical export spanning 21–24 November, a 144-row interim export and a 456-row final export (02:53:18–19:03:24 UTC). The final export contained 453 Grok Bot rows and three Grok Chat rows, all classified as included usage. Overlapping exports are not added together. The final export is used for experimental observations; the historical export is used for cost calibration.

Events were associated with tests using recorded request/response timestamps and screenshots. Multiple events for a single task are summed, including tool calls and unsuccessful attempts when attributable. Timestamp-based attribution is not proof of bot identity; contemporaneous events cannot always be resolved. Dashboard display is rounded and showed an observed delay of about two minutes; exact CSV counters take precedence.

Public extracts remove account email, principal identifiers and billing item IDs. The selected event extract preserves timestamps, test labels and token counters. The calibration extract retains only token counts and historical charges. Unrelated account activity is not included in the public experimental extract.

### 4. Token accounting and monetary estimation

Four counters are reported by the export:

| CSV usage field | Interpretation for this study | Fitted USD per million |
|---|---|---:|
| `prompt-text-tokens` | Prompt tokens recorded separately from cached and cache-write counters | 2.02391839 |
| `cache-write-text-tokens` | Tokens recorded as cache writes | 1.99517634 |
| `cached-prompt-text-tokens` | Cached prompt tokens | 0.49558046 |
| `completion-text-tokens` | Completion tokens, not necessarily visible response text alone | 6.60614410 |

Total recorded tokens are the sum of these four counters over selected events. This is a billing-accounting total, not a measurement of unique text length or context-window capacity. Cached tokens are not assumed free.

The cost model is ordinary least squares through the origin, fitted to 391 Grok Bot historical rows with positive `Pricing Contracted` values in USD. Predictor columns are token counts divided by one million; the dependent variable is the recorded contracted charge. In-sample R² (centered definition) = 0.9672416. No held-out validation was performed. These coefficients are empirical estimates, not official rates; they may absorb model routing or billing effects not present in the export.

Estimated event cost = (2.02391839 × prompt + 1.99517634 × cache write + 0.49558046 × cached prompt + 6.60614410 × completion) / 1,000,000.

Example T01-A: 229 prompt, 58,935 cache write, 27,556 cached prompt and 74 completion tokens = 86,794 recorded tokens; fitted cost $0.132194. The actual recorded additional charge for this included event was $0. The visible answer was `OK`; the request was longer than two characters.

The approximate fourfold difference between prompt and cached prompt rates is a fitted relationship, not a guarantee of savings on a specific interaction. All monetary results below are estimated equivalent usage value, not incremental subscription charges or invoices.

### 5. Experimental protocols and observations

**T01 — Baseline, context reuse and empty task checks.** Prokop was asked: `Reply with exactly one word: OK. Do not use any tools, access any files, contact other bots, or perform any additional tasks.` Repeat at 09:44, 09:47 and 09:49; at 09:55 the same prompt was sent in a group chat with the same agent. The first run recorded 86,794 tokens ($0.1322); the second 87,455 ($0.0451), a 65.9% estimated cost reduction despite more recorded tokens. The group chat did not establish a fresh context. At 09:57 the agent checked its Command Center queue and returned NO_TASKS: 182,082 tokens ($0.0961). A scheduled routine was requested at 10:01, but its eventual execution was delayed and encountered an authentication/agent identity error. The scheduled-run cost is not isolated; omit it from quantitative conclusions. The exact full queue-check and scheduling prompts still require transcription from the original experiment log.

**T02 — Fresh agent baseline.** Create TokenLab without project-specific instructions; observe its automatic onboarding message at 10:12. Send the T01 one-word prompt at 10:13 and repeat at 10:16. Onboarding: 49,516 tokens; replies: 51,110 and 51,747. Other agent activity followed around 10:17–10:19 and is not included. A new agent is not equivalent to a clean model context because account-level profile information may still be available.

**T03 — Persistent memory.** Ask TokenLab to inspect memory metadata (10:21). It reported zero agent-specific entries and approximately 37–39 shared profile entries. Add 20 fictional ExampleLab entries (~9,300 characters, agent-reported), then repeat the one-word prompt at 11:38 and 11:39. Delete those 20 entries and repeat at 11:46 and 11:49; send the same prompt in a group chat at 11:57. Selected comparison: before memory addition 51,747 tokens; after addition 68,439; after deletion 81,498; group chat 82,612. Memory removal did not reduce total recorded usage in this sequence. Conversation history was accumulating and tool interactions also changed the context. The experiment cannot identify the independent effect of stored memory. Exact memory-management prompts still require transcription.

**T04 — Batching.** Send ten separate prompts of the form `Convert N kilograms to grams. Reply with the number only. Do not use any tools or perform additional tasks.` (N=1–10). Compare to one request containing all ten conversions. Ten separate requests: 868,250 tokens, $0.448568; batched: 90,389 tokens, $0.046788. Reduction: 89.59% in recorded tokens and 89.57% in estimated cost. This is a sequential comparison of trivial tasks, not a general batching discount. The exact batch prompt and response should be archived before final release.

**T05 — Delegation.** Direct request: `What is 25 multiplied by 4? Reply with the number only. Do not use any tools, contact other bots, or perform additional tasks.` The delegated variant asked TokenLab to send the same calculation to Prokop and relay his answer. Direct execution: 91,028 tokens ($0.046908); delegated execution: 675,715 tokens across seven events ($0.456415), 9.73 times the estimated cost. The direct event is attributed to 12:06:46; the 12:05 event belongs to T04-B. Two agents were involved, not a six-agent committee. The exact delegation prompt requires transcription.

**T06 — Ordinary communication.** Send short natural-language messages to established bots, without constraining the reply. Prokop and Anička reacted to OK with thumbs-up and to Thank you! with hearts. Filip replied to Good morning! after a longer gap and reacted to Good evening! shortly afterward. Astrid answered How are you today?; Markéta answered What are you currently working on?; Gregory suggested priorities. Agent, cache state, conversation context and response length differed. These observations show possible communication overhead, not a controlled comparison of phrases or agents.

| Test | Message | Recorded tokens | Estimated USD |
|---|---|---:|---:|
| T06-A1 | OK | 103,538 | 0.0540 |
| T06-A2 | OK | 57,172 | 0.0732 |
| T06-B1 | Thank you! | 104,215 | 0.0536 |
| T06-B2 | Thank you! | 57,825 | 0.0410 |
| T06-C1 | Good morning! | 84,951 | 0.1298 |
| T06-C2 | Good evening! | 85,581 | 0.0446 |
| T06-D1 | How are you today? | 102,405 | 0.1999 |
| T06-E1 | What are you currently working on? | 87,181 | 0.1347 |
| T06-F1 | Request for today's priorities (wording to confirm) | 57,066 | 0.0744 |

**T07 — Selective retrieval (delta processing).** Generate a CSV of 100 fictional business emails, 95 marked processed and five unprocessed (IDs 96–100). First ask TokenLab to read the entire file without a filtering script and summarize unprocessed records. Its file reader exposed only IDs 1–21 and 92–100 in full; it nevertheless identified the five intended records. Next ask it to use deterministic filtering and analyze only the five returned records. Attempted full read: 418,712 tokens, $0.232751; filter first: 222,595 tokens, $0.121081. Estimated cost reduction 47.98%. The first read was incomplete and the second run already had prior knowledge; this comparison does not establish a controlled savings rate for production systems or Gmail APIs. The 1,000-order illustration in the article is hypothetical.

**T08 — Report length.** Use a script to retrieve the same five unprocessed records, then analyze business implications, priorities, risks and actions. Compare a detailed report with a concise table (Email ID, Priority, Required action, maximum 25 words per action; no introduction or detailed reasoning). Detailed: 232,695 tokens, $0.154830; concise: 242,380 tokens, $0.134998. Completion tokens fell from 5,756 to 582; estimated cost fell 12.81% despite 4.16% more total recorded tokens. The outputs differ in some priorities, and the concise report followed the detailed report in the same conversation. They are not established as equivalent in analytical quality. The full detailed-report prompt should be archived.

**T09 — Deterministic automation.** Using the same CSV, identify subjects containing the word invoice (case-insensitive) and extract Email ID, Sender, Subject, Invoice amount, Currency and Payment terms. T09-A initially used manual AI extraction without filtering scripts; concurrent Astrid activity made that run ambiguous. T09-A2 repeated the extraction from scratch into `accounting_manual_v2.csv`. Three screenshot-matched events are used; a fourth event at 18:54:44 is excluded because its attribution is unresolved. T09-B instructed the agent to create but not execute a reusable Python script, without hardcoded records or AI APIs, with explicit exception handling. T09-C executed it once and reported counts and output path; a first timing-tool attempt failed before actual script execution, and its overhead is included. T09-V compared the manual and automated results and exported files. T09-D executed the supplied script independently outside Grok Bot.

| Test | Operation | Recorded tokens | Estimated USD |
|---|---|---:|---:|
| T09-A2 | Manual AI extraction | 484,994 | 0.286929 |
| T09-B | Build script | 169,012 | 0.148701 |
| T09-C | Agent executes script | 176,761 | 0.093353 |
| T09-V | Validate and export | 122,050 | 0.070167 |
| T09-D | Independent script execution | 0 LLM tokens | 0 LLM usage |

The supplied script was independently rerun during preparation of this draft. It produced nine records, zero exceptions and a byte-identical result to the original automated CSV. The two supplied manual and automated CSVs match in all 54 parsed field values. This demonstrates agreement for the synthetic dataset, not accuracy on arbitrary real invoices. The script uses fixed regular expressions, standard-library CSV and Decimal processing; it is not an invoice attachment parser. Its independent execution requires ordinary computing resources. The reported 0.042-second runtime was measured by TokenLab, not a standardized performance benchmark.

### 6. Financial projections

Projections hold the observed per-operation estimated usage values constant, assuming comparable workload, cache conditions and frequency. These are scenario calculations, not forecasts of invoices. No double-counting across overlapping scenarios is intended.

Communication scenario: seven agents, 14 OK messages/day, seven thank-you messages/day, 1.5 morning greetings/day, 1.5 social questions/day, seven status checks/day, three planning requests/day. Average the two observations for OK and thank-you; use the corresponding individual observations for the other categories. At 30 days/month and 12 months/year, the fitted model produces ~$86.45/month or ~$1,037.42/year. Some communication is valuable, so this is not all avoidable waste.

Empty checks: 5 bots × 4 checks/hour × 24 hours × 30 days = 14,400 checks/month. At $0.096142 per check this represents ~$1,384/month if all checks are empty and behave like T01-B. An event-driven workflow would still have infrastructure and actual work costs.

Delta processing: ($0.232751 − $0.121081) × 7 workflows × 3 runs/day × 360 days ≈ $844/year.

Accounting automation: setup + validation = $0.218868; recurring modeled saving when an agent runs the script = $0.286929 − $0.093353 = $0.193576/run; break-even = ceiling(0.218868 / 0.193576) = 2 runs. Independent execution has zero recurring LLM usage, so the modeled setup cost is recovered after one run, excluding infrastructure and maintenance. For seven separate workflows running three times daily for 365 days, manual AI usage is approximately $2,199; independent execution has ~$1.53 combined AI setup cost. Costs of maintenance, computing and production validation are not included. The observed context reduction between T09-A2 and T09-B/C may contribute to the difference; it cannot all be causally attributed to scripting.

### 7. Limitations and publication cautions

- Single account, one day, small sample sizes; no randomized order or repeated independent trials for most tests.
- Cache state, conversation history, model routing and agent configuration were not fully controlled.
- Billing events are account-level, not agent-level. Some runs have ambiguous attribution; selected rows are documented in the event extract.
- Historical cost regression is in-sample, and is not official pricing. Included usage may have zero marginal cash cost until allowance is exceeded.
- Token totals include separately reported cache counters and are not unique input tokens.
- Test fixtures are synthetic and consistently formatted; generalization to real data, attachment parsing or third-party APIs is untested.
- Report length and task completion quality are different metrics. The T07 full read was incomplete and the T08 priority judgments differed.
- Do not interpret cold/warm cache as fully uncached versus fully cached; both runs contained cached tokens. No tools were requested in T01-A and tool use was not established.
- Original prompt transcripts for several tests remain incomplete in this release; reconstructed instructions must not be presented as verbatim prompts.

### 8. Reproduce the experiment

1. Record account configuration, agent identity, model selection (if exposed), UTC timestamps and current conversation state.
2. Reduce unrelated agent activity where possible. Record any overlap instead of silently assigning ambiguous events.
3. Run paired tasks with identical objectives, repeat several times and alternate order. Separate fresh-agent and repeated-context experiments.
4. Export usage CSV after events appear. Keep exact counters, aggregate all attributable events and document exclusions.
5. Fit pricing coefficients on paid records if an applicable official rate is unavailable; report assumptions and fit limitations.
6. Compare outputs for correctness and completeness before calculating savings. Report both usage and quality.
7. For the accounting example, use the included synthetic CSV and script. Run locally with Python 3 (no third-party dependencies):

```sh
python scripts/accounting_processor.py data/tokenlab_emails.csv reproduced.csv reproduced_exceptions.csv
```

Compare parsed rows with `accounting_automated.csv` and `accounting_manual_v2.csv`. Expected: nine rows, six matching fields per row and zero exceptions.

### 9. Supporting materials

- `pricing_calibration_anonymized.csv`: 391 historical positive-charge rows, token counters and contracted price only.
- `experiment_events_anonymized.csv`: selected experimental events with assigned test IDs, exact counts and modeled cost.
- `experiment_summary.csv`: grouped totals by test ID.
- `tokenlab_emails.csv`: synthetic fixture (100 records).
- `accounting_processor.py`: original deterministic implementation.
- `accounting_manual_v2.csv` and `accounting_automated.csv`: original comparison outputs.
- `reproduce_costs.py`: refit cost model and regenerate grouped experimental totals from the public extracts.

### 10. Version history

v0.1 — Initial review draft. Refit pricing model from original billing exports, selected exact events, and reran accounting script. Remaining before public release: archive complete verbatim prompts, review ambiguous event assignments, reconcile article and infographic claims with this document, and approve public extracts. No peer review or platform endorsement is implied.


v0.2 — Added the correction policy and change register below. No experimental data, pricing coefficients or findings were changed in this revision.

### 11. Corrections, transparency and change register

This study is maintained as a versioned research record. Readers may submit suspected errors, contradictory observations or independent reproductions through the issue tracker of the public research repository (https://github.com/Allegorise/grokbots-hidden-cost-experiments) once it is available. Reference the experiment ID, affected claim, release version and supporting evidence.

**Correction procedure**

1. Record the report and assign a unique correction ID. Preserve the original published wording, figure or dataset and its release version.
2. Verify against original evidence, documented event attribution, calculation scripts and the numerical source of truth (internal document 07). Distinguish a confirmed error from a new finding or an unresolved interpretation.
3. Record the corrected value or wording, rationale, supporting evidence and effect on conclusions or financial projections. If a number cannot be verified, mark it as unresolved rather than inventing a replacement.
4. Review affected CSV extracts, scripts, methodology, website articles, X Articles, LinkedIn posts, graphics and promotional claims. Recalculate dependent values and rerun relevant reproduction checks before approving changes.
5. Publish a dated change entry and a new version/tag. Preserve previous releases; never silently replace a published experimental result. For material errors, add a prominent correction to the affected article or publish a linked correction where editing is unavailable. Pause reuse of affected promotional assets until corrected.
6. Close the correction only after all affected assets have been updated or explicitly marked as superseded. Do not expose private billing records, credentials or personal information in public evidence.

**Versioning:** pre-release drafts use v0.x; the first approved public release is v1.0. Use a patch release for editorial or narrowly scoped corrections, a minor release for additional evidence or extensions, and a major release for substantial methodological changes. Any material correction must be explicitly described regardless of its version number.

**Change register (template; no public corrections have been issued yet)**

| Correction ID | Reported / resolved date (UTC) | Affected version and test ID | Original claim | Revised claim | Evidence / rationale | Impact on conclusions | Affected assets | Status | Release |
|---|---|---|---|---|---|---|---|---|---|
| COR-001 onward | — | — | — | — | — | — | — | — | — |

Status values: reported, investigating, confirmed, rejected with rationale, corrected, published, closed. The existing pre-publication issues in internal document 07 are review items, not previously published corrections. Record any confirmed corrections when the release is finalized.


RC1: dataset bytes unchanged; portable script paths and automated tests added. See [data provenance](data_provenance.md) for audit scope and unresolved attribution.

v1.0: version identifiers finalized; dataset bytes, algorithms and results unchanged. Publication of historical contracted charges and exact UTC timestamps approved by the founder with residual risks accepted; infographics are not part of this release.
