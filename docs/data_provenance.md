# Data provenance and publication audit

The six CSV files are byte-identical to the supplied Public Research REVIEW v0.2 archive. The private internal v2 archive contains the raw billing exports and evidence; it must not be published.

## Calibration

Historical export: 500 rows. Select Product = grok-bot, Pricing Currency = USD, Pricing Contracted > 0. Retain the four integer usage counters and contracted price. The multiset of these tuples (including multiplicity) matches all 391 public rows exactly. OLS through the origin uses token counts in millions. No held-out validation. Prices are historical contracted values, not official prices.

## Experimental selection

Final export: 456 rows (453 Grok Bot, 3 Grok Chat); interim export: 144 rows. Overlapping exports are not summed. Each of the 74 public selected rows matches exactly one Grok Bot row in the final export by UTC timestamp and four counters. Test IDs are analyst assignments from the experiment log and screenshots, not billing metadata. Remaining 379 Grok Bot and 3 Grok Chat rows are not selected; a complete row-by-row exclusion rationale is unavailable. T09-A initial run overlaps unrelated activity; 18:54:44.706Z is excluded due to uncertain attribution. T01-C0 is routine setup, not an isolated scheduled run. T07 full read incomplete; T08 priorities differ. Full verbatim prompts and independent attribution of every event remain incomplete. See methodology for experiment-specific caveats.

## Privacy and publication decisions

Public calibration drops timestamps, account email, principal and billing IDs; experimental extract retains precise UTC timestamps, assigned test IDs and usage counters. Synthetic fixture uses fictional .example addresses. No raw export or screenshot is included. Precise times and contracted prices may still enable linkage or disclose commercially sensitive information. The founder approved publication of the historical contracted charges and exact UTC timestamps and accepted the residual contractual-disclosure and timestamp-correlation risks. Public users can reproduce computations but cannot independently verify private raw-source attribution. Infographics are not part of this release. Website articles are separate works and are not reconciled in this package.

## AI assistance

The research package was assembled and locally tested with the assistance of ChatGPT (OpenAI). Repository preparation, validation and release engineering were assisted by Claude (Anthropic). Research design, data selection, interpretation and release decisions remain the responsibility of Allegorise.

Audit date: 2026-11-26. Original inputs remain untouched.
