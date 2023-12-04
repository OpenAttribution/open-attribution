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
    "attributed_events",
    "attributed_events_mv",
    "daily_overview",
    "daily_overview_impressions_mv",
    "daily_overview_clicks_mv",
]


for my_table in my_tables:
    # Check if the table exists
    table_exists = client.command(f"EXISTS TABLE {my_table}")
    if not table_exists:
        print(f"{my_table=} create table")
        with open(f"sql/create/{my_table}.sql") as file:
            create_impressions_table_query = file.read()
        client.command(create_impressions_table_query)
    else:
        print(f"{my_table=} exists")
