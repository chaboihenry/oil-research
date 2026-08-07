import os
from dotenv import load_dotenv
import requests
from pathlib import Path
import json
import pandas as pd


ROOT_DIR = Path(__file__).parent.parent
TRADE_FLOWS_DIR = ROOT_DIR / 'data' / 'raw'/ 'trade-flows'
print(TRADE_FLOWS_DIR)

load_dotenv()
API_KEY = os.getenv("EIA_API_KEY")
# https://www.eia.gov/opendata/browser/petroleum/move/impcus
api_url = "https://api.eia.gov/v2/petroleum/move/impcus/data/"

Params = {
    "api_key": API_KEY,
    "frequency": "monthly", 
    "data[0]": ["value"],
    "facets[product][]": ["EPC0"],
    "facets[process][]": ["IM0"],
    "start": "2019-01", 
    "end": "2026-05", 
    "sort[0][column]" : "period",
    "sort[0][direction]": "asc",
    "length": 5000,
    "offset": 0
}

try:
    response = requests.get(api_url, params=Params)
    response.raise_for_status()
    payload = response.json()
    del payload['request']['params']['api_key']
    with open(TRADE_FLOWS_DIR / "eia-impcus-crude-2019-01-to-2026-05_retrieved-2026-08-04.json", "w", encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)

except requests.exceptions.RequestException as e:
    print(f"API Request Failed: {e}")

print("Raw JSON file saved successfully")

# converting to dataframe to save as csv
df = pd.DataFrame(payload['response']['data'])
# duoarea 52, area-name 49, series 104 unqiue values with a 4486 row dataset, converted to category dtype.
columns = ['duoarea', 'area-name']
# ['product', 'product-name', 'process', 'process-name'] all have 1 unique values (columns filtered on api call)
df.drop(columns=['product', 'product-name', 'process', 'process-name', 'series', 'series-description'], inplace=True)
for col in columns:
    df[col] = df[col].astype("category")
df['period'] = pd.to_datetime(df['period'])
df['value'] = df['value'].astype('int64')
# MBBL = 1000 barrels of crude oil
df = df[df['units'] == 'MBBL']
df.reset_index(drop=True, inplace=True)
# some rows in the dataset are already aggregated
mask = (df['duoarea'].isin(['NUS-ME0', 'NUS-MN0', 'NUS-MP0', 'NUS-Z00']))
df['is_aggregate'] = mask
# checking aggregates
non_aggregate = df[~df['is_aggregate']].groupby('period')['value'].sum()
duplicates = df.duplicated(subset=['period','duoarea']).sum()
print(non_aggregate, df[df['duoarea'] == 'NUS-Z00'], duplicates)
df.to_csv(ROOT_DIR / 'data' / 'processed' / 'us-crude-imports-by-origin-monthly.csv', index=False)


