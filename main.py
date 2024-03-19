from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import json
import os

output_dir = "region_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

df = pd.read_csv('cum.csv', sep=',')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('г ', '')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('обл', 'область')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Респ', 'Республика')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('АО ', '')

df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Аобласть Еврейская', 'Еврейская область')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Кемеровская областьасть - Кузбасс область', 'Кемеровская область')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Чувашия Чувашская Республикаублика -', 'Чувашская область')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Республика Донецкая Народная', 'Донецкая область')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Республика Луганская Народная', 'Луганская область')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Республика Саха /Якутия/', 'Республика Саха')
df['ФИАС Регион'] = df['ФИАС Регион'].str.replace('Ханты-Мансийский Автономный окру- Югра', 'Ханты-Мансийский округ')

df = df[:1000]

unique_regions = df['ФИАС Регион'].unique()

region_dfs = {}
for region in unique_regions:
    region_dfs[region] = df[df['ФИАС Регион'] == region]

for region, region_df in region_dfs.items():
    output_file = os.path.join(output_dir, f"{region}.csv")
    region_df.to_csv(output_file, index=False)

result = df.to_dict(orient='records')
regions = [os.path.splitext(f)[0] for f in os.listdir('region_data') if f.endswith('.csv')][:10]

#%%
with open('map.html', 'r', encoding='utf-8') as f:
    template_str = f.read()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    template = Template(template_str)
    return template.render(data=result, regions=regions)
