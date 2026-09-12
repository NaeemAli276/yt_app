from keras.ops import view
from matplotlib.image import thumbnail
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
import uvicorn

from yt_ftns import search_yt, download_song_selected_song

app = FastAPI(title='yt_api')

origins = [
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path='/{query}')
async def get_songs(query):

    return search_yt(query)

@app.post('/download/')
async def download_song(url):
    download_song_selected_song(url)

if __name__ == '__main__':
    uvicorn.run(app)