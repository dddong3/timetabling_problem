import json
import os
from fastapi import FastAPI, Response, Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn
import requests
import time
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from genetic_algo import GeniticAlgoithm

app = FastAPI(title="course table planner")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    response = RedirectResponse(url="/docs")
    return response


### chromosome ###
@app.get("/chromosome/{filename}")
async def get_chromosome(request: Request, filename: str):
    files = os.listdir('chromosome')
    chromosome_list = [file.split('.')[0] for file in files]
    if filename not in chromosome_list:
        return 404
    test_chromosome = json.load(open('chromosome/' + filename + '.json', 'r'))
    return test_chromosome

@app.get("/chromosome")
async def get_chromosome_list(request: Request):
    files = os.listdir('chromosome')
    chromosome_list = [file.split('.')[0] for file in files]
    return chromosome_list

@app.post("/chromosome")
async def post_chromosome(request: Request, live: int = 20, popu: int = 20, anchors: List[str] = []):
    GeniticAlgoithm.init('test_gene_washed.json', 'class.json', live=live, popu=popu, anchors=anchors)
    ga = GeniticAlgoithm()
    opt_filename = ga.output_chromosome().split('/')[1].split('.')[0]
    return opt_filename

@app.delete("/chromosome/{filename}")
async def delete_chromosome(request: Request, filename: str):
    files = os.listdir('chromosome')
    chromosome_list = [file.split('.')[0] for file in files]
    if filename not in chromosome_list:
        return 404
    os.remove('chromosome/' + filename + '.json')
    files = os.listdir('chromosome')
    chromosome_list = [file.split('.')[0] for file in files]
    return chromosome_list

# uvicorn.run(app, host="0.0.0.0",port=8000)