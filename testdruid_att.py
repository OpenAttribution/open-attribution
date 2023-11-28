import pandas as pd
from pydruid.db import connect

# Establish a connection to Druid
conn = connect(host="localhost", port=8082, path="/druid/v2/sql/", scheme="http")

# Read and format the SQL file
with open("druid_query_impressions.sql") as file:
    sql_query = file.read()

df = pd.read_sql(sql_query, con=conn)
