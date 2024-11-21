from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import pandas as pd

synteny_app = FastAPI()

synteny_app.mount("/static", StaticFiles(directory="static"), name="static") # /static{/something} >> to static folder
templates = Jinja2Templates(directory="templates")

@synteny_app.get("/synteny-graph", response_class=HTMLResponse)
async def synteny_graph_page(request : Request):
    return templates.TemplateResponse(
        request=request, name="synteny_cytoscape.html", context={}
    )

@synteny_app.get("/input-data")
async def send_input():
    node_l = []
    edge_l = []
    for line in open("/Users/charyeongheo/codes/synteny2graph/fastapi_workdir/data/gnnscaff/3kmer_MGW_edge.tsv"):
        line = line.strip()
        if line.startswith('#'):
            continue

        if len(line.split('\t'))<7: continue
        edgeID, previous_nodeID, following_nodeID, species, MGW, kmer, label = line.split('\t')
        node_l.append(previous_nodeID)
        node_l.append(following_nodeID)
        edge_l.append({'id':'e'+edgeID, 'source':previous_nodeID, 'target':following_nodeID, 'feature':"_".join([species,MGW,kmer,label])})

    result = []
    for item in sorted(list(set(node_l))):
        result.append({"data": {"id": item}})

    for item in edge_l:
        result.append({"data": item})
    print(result[0:10])
    print(result[len(result)-10:len(result)])

    return result
    
    # return [ 
    #     { 
    #         "data": { "id": 'a' }
    #     },
    #     { 
    #         "data": { 'id': 'b' }
    #     },
    #     { 
    #         'data': { 'id': '1', 'source': 'a', 'target': 'b' ,'feature': 'testXXX'}
    #     }
    # ]
    
# 기본 경로에서 확인
@synteny_app.get("/")
def read_root():
    return {"message": "Welcome to the Local TSV Processing API"}
