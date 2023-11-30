import clickhouse_connect

client = clickhouse_connect.get_client(host="localhost")

my_tables = [
    "impressions",
    "impressions_queue",
    "impressions_mv",
    "clicks",
    "clicks_queue",
    "clicks_mv",
    "events",
    "events_queue",
    "events_mv",
]


for my_table in my_tables:
    # Check if the table exists
    table_exists = client.command(f"EXISTS TABLE {my_table}")
    if not table_exists:
        print(f"{my_table=} create table")
        with open(f"sql/ch_create_table_{my_table}.sql", "r") as file:
            create_impressions_table_query = file.read()
        client.command(create_impressions_table_query)
    else:
        print(f"{my_table=} exists")
