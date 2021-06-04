from typing import Optional
from fastapi import FastAPI
import sqlalchemy

app = FastAPI(docs_url='/docs', openapi_prefix='/')

@app.get("/")
def read_root():
    return {"Hello": sqlalchemy.__version__}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    import uvicorn
    reload = True
    uvicorn.run("main:app", host='0.0.0.0', port=8009, reload=reload)