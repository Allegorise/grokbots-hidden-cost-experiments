"""Refit the empirical USD cost model and summarize selected events. Requires pandas and numpy."""
from pathlib import Path
import numpy as np
import pandas as pd
p = Path(__file__).resolve().parent.parent / "data"
keys = ['cache-write-text-tokens','cached-prompt-text-tokens','completion-text-tokens','prompt-text-tokens']
h = pd.read_csv(p/'pricing_calibration_anonymized.csv')
X = h[keys].to_numpy()/1e6
y = h['Pricing Contracted'].to_numpy()
b = np.linalg.lstsq(X,y,rcond=None)[0]
print(dict(zip(keys,b)))
print('R²:',1-((y-X@b)**2).sum()/((y-y.mean())**2).sum())
d = pd.read_csv(p/'experiment_events_anonymized.csv')
d['estimated_usd'] = d[keys].to_numpy()@b/1e6
d['total_tokens'] = d[keys].sum(axis=1)
print(d.groupby('test_id').agg(events=('total_tokens','size'),tokens=('total_tokens','sum'),cost=('estimated_usd','sum')).to_string())
