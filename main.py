from fastapi import FastAPI,Depends,HTTPException
from typing import AsyncContextManager
from sqlmodel import Session,select

from models.zapatilla import Zapatilla


import uvicorn


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
