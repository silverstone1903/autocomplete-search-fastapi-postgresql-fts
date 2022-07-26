# https://www.freecodecamp.org/news/fuzzy-string-matching-with-postgresql/
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")

templates = Jinja2Templates(directory="./templates")
app = FastAPI(title="Data API")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

local = False
if local:
    engine = create_engine(
        "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
    )

else:
    engine = create_engine("postgresql+psycopg2://postgres:123456@db:5432/postgres")


@app.get("/health", status_code=200, summary="Returns HC Page.", tags=["hc"])
async def home():
    return {"message": "Still Alive"}


@app.get("/", status_code=200, summary="Returns Search Page.", tags=["search"])
def root(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "home.html", context={"request": request, "result": result}
    )


@app.get("/fts", status_code=200, summary="Returns FTS Matches.", tags=["search"])
async def match_ts(term: str):
    if len(term) > 1:
        q = """select "movie_name" from movies t where ts @@ plainto_tsquery('simple', '{0}:*') limit 10;""".format(
            term
        )
        res = engine.execute(q).fetchall()
        if len(res) > 0:
            return [res[c][0] for c in range(len(res))]
        else:
            return "Sonuç Bulunamadı"
    else:
        return "Sonuç Bulunamadı"


@app.get("/trgm", status_code=200, summary="Returns Trigram Matches.", tags=["search"])
async def match_any(term: str):
    if len(term) > 1:
        q = """SELECT "movie_name" FROM movies t WHERE '{0}' %% 
        ANY(STRING_TO_ARRAY(t."movie_name" ,' ')) limit 10;""".format(
            term
        )

        res = engine.execute(q).fetchall()
        if len(res) > 0:

            return [res[c][0] for c in range(len(res))]
        else:
            return "Sonuç Bulunamadı"
    else:
        return "Sonuç Bulunamadı"
