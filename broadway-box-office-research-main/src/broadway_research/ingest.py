from pathlib import Path
import pandas as pd

def load(path):
    sheets=pd.read_excel(next(Path(path).glob('*.xlsx')),sheet_name=None)
    p=next(x for x in sheets.values() if 'Show' in x.columns)
    m=next(x for x in sheets.values() if 'week_ending' in x.columns)
    m['week_ending']=pd.to_datetime(m.week_ending,errors='raise')
    return p,m
