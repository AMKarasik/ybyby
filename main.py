from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

df = pd.read_csv('cum.csv', sep=',')

result = df.to_dict(orient='records')
regions = sorted(list(set(df["ФИАС Регион"])))

#%%
with open('map.html', 'r', encoding='utf-8') as f:
    template_str = f.read()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    template = Template(template_str)
    return template.render(data=result, regions=regions)
