import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import io
import warnings

warnings.filterwarnings("ignore")


def psql_insert(engine, table_name, df):
    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep="\t", header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, table_name, null="")
    conn.commit()


local = False  # Docker
if local:
    engine = create_engine(
        "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
    )
    df = pd.read_feather("data/movies.feather")
else:
    engine = create_engine("postgresql+psycopg2://postgres:123456@db:5432/postgres")
    df = pd.read_feather("/app/data/movies.feather")

# create ddl codes using pandas
table = "movies"
ddl = pd.io.sql.get_schema(df, table, con=engine)
print(ddl)


# create table using dtypes
engine.execute("DROP TABLE IF EXISTS {0}".format(table))
print("Dropped table if exists")
engine.execute(ddl.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS"))
print("Created table")
psql_insert(engine, table, df)
print("Data insert completed.")

q = """
    alter table {0} add column ts tsvector
    generated always as (to_tsvector('simple', "movie_name")) stored
    """.format(
    table
)
engine.execute(q)
print("TSVector created for {}.".format("movie_name"))

q = """
drop index if exists ts_index;
create index ts_idx on
{0}
using GIN (ts)
""".format(
    table
)
engine.execute(q)
print("Index created for ts.")

q = """
CREATE EXTENSION IF NOT EXISTS pg_trgm;
"""
engine.execute(q)
print("Extension created for pg_trgm.")
print("Done.")
