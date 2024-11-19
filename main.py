from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
    return [ 
        { 
            "data": { "id": 'a' }
        },
        { 
            "data": { 'id': 'b' }
        },
        { 
            'data': { 'id': 'ab', 'source': 'a', 'target': 'b' ,'feature': 'testXXX'}
        }
    ]