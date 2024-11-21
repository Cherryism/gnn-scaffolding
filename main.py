from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import pandas as pd

synteny_app = FastAPI()
# 서버 내 TSV 파일의 기본 경로
BASE_DIR = Path(__file__).resolve().parent
TSV_DIR = BASE_DIR / "data/gnnscaff"  # 예: 모든 TSV 파일을 data 디렉토리에 저장

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
@synteny_app.get("/process-tsv/")
async def process_tsv(file_name: str):
	"""
	서버 디렉토리에 저장된 TSV 파일을 처리하는 API
	:param file_name: 처리할 TSV 파일 이름
	"""
	file_path = TSV_DIR / file_name

	# 파일 존재 여부 확인
	if not file_path.exists() or not file_path.is_file():
		raise HTTPException(status_code=404, detail="TSV file not found")

	try:
		# TSV 파일 읽기
		df = pd.read_csv(file_path, sep="\t")

		# 데이터 처리 예시 (여기에서 원하는 로직을 추가)
		processed_data = df.head(5)  # 예: 첫 5행 반환

		# 결과 반환
		return {
			"file_name": file_name,
			"columns": df.columns.tolist(),
			"sample_data": processed_data.to_dict(orient="records")
		}

	except Exception as e:
		raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {e}")

# 기본 경로에서 확인
@synteny_app.get("/")
def read_root():
    return {"message": "Welcome to the Local TSV Processing API"}
