# Data dictionary

All files are UTF-8 CSV with headers. Monetary values are USD unless specified otherwise. Token counters are nonnegative integers, separately reported billing counters, not unique context lengths.

| File | Field | Meaning |
|---|---|---|
| pricing_calibration_anonymized.csv; experiment_events_anonymized.csv | cache-write-text-tokens | Cache write tokens |
| same | cached-prompt-text-tokens | Cached prompt tokens |
| same | completion-text-tokens | Completion tokens, not necessarily visible response only |
| same | prompt-text-tokens | Separately recorded prompt tokens |
| pricing_calibration_anonymized.csv | Pricing Contracted | Historical contracted USD charge, positive |
| experiment_events_anonymized.csv | test_id | Analyst-assigned test group |
| same | Event Time | UTC ISO timestamp |
| same | total_tokens | Sum of four counters |
| same | estimated_usd | Fitted usage value, not incremental charge |
| experiment_summary.csv | test_id | Test group |
| same | events | Count of selected rows |
| same | tokens | Sum of total_tokens |
| same | cost | Sum of modeled USD values |
| tokenlab_emails.csv | ID | Synthetic email identifier |
| same | date | Synthetic date/time, timezone unspecified |
| same | sender | Fictional sender and .example email |
| same | subject | Fictional subject |
| same | body | Fictional message text |
| same | processed | Fixture processing status |
| accounting_manual_v2.csv; accounting_automated.csv | Email ID | Source synthetic ID |
| same | Sender | Copied sender |
| same | Subject | Copied subject |
| same | Invoice amount | Parsed positive decimal amount |
| same | Currency | Currency code |
| same | Payment terms | Extracted payment terms |
