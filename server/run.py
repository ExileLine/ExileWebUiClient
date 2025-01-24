# -*- coding: utf-8 -*-
# @Time    : 2025/1/23 18:02
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : run.py
# @Software: PyCharm


import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"code": 200}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
