import pandas as pd
from pathlib import Path
from tabulate import tabulate

class TraceabilityBuilder:
    def __init__(self, run_dir):
        self.run_dir = Path(run_dir)

    def discover(self):
        feats = list((self.run_dir / 'features').glob('*.feature'))
        tests = list((self.run_dir / 'tests').glob('test_*.py'))
        rows = []
        for f in feats:
            req_id = f.name.split('_',1)[0]
            linked = [t for t in tests if f"test_req_{req_id}.py"==t.name]
            for t in linked or [None]:
                rows.append({'RequirementID': req_id,'FeatureFile': f.name,'TestFile': t.name if t else '','Status':'Generated'})
        return rows

    def build(self, csv_out, html_out=None):
        rows = self.discover()
        df = pd.DataFrame(rows).sort_values(['RequirementID','TestFile'])
        Path(csv_out).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_out, index=False)
        if html_out:
            Path(html_out).parent.mkdir(parents=True, exist_ok=True)
            df.to_html(html_out, index=False)
        print(tabulate(df.head(20), headers='keys', tablefmt='github'))
