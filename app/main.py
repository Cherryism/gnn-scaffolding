from typing import List, Optional
from fastapi import FastAPI, Query
from resolver import random_items,random_genres_items
from recommender import item_based_recommendation, user_based_recommendation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Hello World"}

@app.get("/all/")
async def all_movies():
    result = random_items()
    return {"result":result}

@app.get("/genres/{genre}")
async def genre_movies(genre: str):
    result = random_genres_items(genre)
    return {"result": result}

@app.get("/user-based/")
async def user_based(params: Optional[List[str]] = Query(None)):
    #Optional[List[str]]는 fastAPI에서 url parameter를 사용하기 위한 기본적인 형태
    input_ratings_dict = dict(
		(int(x.split(":")[0]), float(x.split(":")[1])) for x in params
	)
    result = user_based_recommendation(input_ratings_dict)
    return {"result": result}

@app.get("/item-based/{item_id}")
async def item_based(item_id: str):
    result = item_based_recommendation(item_id)
    return {"result": result}