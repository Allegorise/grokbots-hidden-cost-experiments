import csv
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
KEYS = ['cache-write-text-tokens','cached-prompt-text-tokens','completion-text-tokens','prompt-text-tokens']

class Reproduction(unittest.TestCase):
    def test_checksums(self):
        for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
            digest, path = line.split('  ', 1)
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest, path)

    def test_costs(self):
        h = pd.read_csv(ROOT/'data/pricing_calibration_anonymized.csv')
        self.assertEqual(len(h), 391)
        X = h[KEYS].to_numpy()/1e6
        y = h['Pricing Contracted'].to_numpy()
        b = np.linalg.lstsq(X,y,rcond=None)[0]
        np.testing.assert_allclose(b,[1.99517634,0.49558046,6.60614410,2.02391839],rtol=0,atol=1e-8)
        self.assertAlmostEqual(1-((y-X@b)**2).sum()/((y-y.mean())**2).sum(),0.9672415555,places=9)
        d = pd.read_csv(ROOT/'data/experiment_events_anonymized.csv')
        self.assertEqual(len(d),74)
        self.assertEqual(d['Event Time'].nunique(),74)
        np.testing.assert_array_equal(d[KEYS].sum(axis=1),d.total_tokens)
        cost = d[KEYS].to_numpy()@b/1e6
        np.testing.assert_allclose(cost,d.estimated_usd,rtol=0,atol=1e-9)
        d['estimated_usd']=cost
        got=d.groupby('test_id').agg(events=('total_tokens','size'),tokens=('total_tokens','sum'),cost=('estimated_usd','sum')).sort_index()
        expected=pd.read_csv(ROOT/'data/experiment_summary.csv').set_index('test_id').sort_index()
        self.assertEqual(len(got),39)
        pd.testing.assert_frame_equal(got[['events','tokens']],expected[['events','tokens']])
        np.testing.assert_allclose(got.cost,expected.cost,rtol=0,atol=1e-9)
        subprocess.run([sys.executable,str(ROOT/'scripts/reproduce_costs.py')],check=True,capture_output=True)

    def test_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out.csv'; exc=Path(tmp)/'exceptions.csv'
            run=subprocess.run([sys.executable,str(ROOT/'scripts/accounting_processor.py'),str(ROOT/'data/tokenlab_emails.csv'),str(out),str(exc)],check=True,capture_output=True,text=True)
            self.assertIn('Processed records: 9',run.stdout)
            self.assertIn('Exceptions: 0',run.stdout)
            self.assertFalse(exc.exists())
            self.assertEqual(out.read_bytes(),(ROOT/'results/accounting_automated.csv').read_bytes())
            def rows(p):
                with p.open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
            a=rows(out); m=rows(ROOT/'results/accounting_manual_v2.csv')
            self.assertEqual(len(a),9)
            self.assertEqual(sum(map(len,a)),54)
            self.assertEqual(a,m)
