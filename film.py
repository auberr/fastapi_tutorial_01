from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

# note : normally you'd want to use migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_films = db.query(models.Film).count()
    if num_films == 0:
        films = [
            {'name': 'Blade Runner', 'director':'Ridley Scott'},
            {'name': 'Pulp Fiction', 'director':'Quentin Tarantino'},
            {'name': 'Mulholland Drive', 'director':'David Lynch'},
            {'name': 'Jurassic Park', 'director':'Steven Spielberg'},
            {'name': 'Tokyo Story', 'director':'Yasujiro Ozu'},
            {'name': 'Chungking Express', 'director':'Kar-wai Wong'},
        ]
        for film in films:
            db.add(models.Film(**film))
        db.commit()
    else:
        print(f"{num_films} films already in DB")


@app.get('/index/', response_class=HTMLResponse)
async def movielist(
    request: Request, 
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    page: int  = 1
    ): #hx-request
    # hard coding db version
    # films = [
    #     {'name': 'Blade Runner', 'director': 'Ridley Scott'},
    #     {'name': 'Pulp Fiction', 'director': 'Quentin Tarantino'},
    #     {'name': 'Mulholland Drive', 'director': 'David Lynch'}
    # ]

    # db connected
    N = 2
    OFFSET = (page - 1) * N
    films = db.query(models.Film).offset(OFFSET).limit(N)
    print(films)
    context = {'request': request, 'films': films, "page": page}
    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})