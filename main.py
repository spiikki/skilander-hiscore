# Skilander HiScore API
# 2024 hemohespiikki of hiihtoliitto

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "success"}