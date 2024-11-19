#!/bin/bash
set -e

# Path to your directory
INIT_SQL_DIR="/my-tables"

if [ -f /.dockerenv ]; then
	export ISDOCKER=true
else
	export ISDOCKER=false
fi

# Wait for ClickHouse server to start
until clickhouse-client --host localhost --query "SELECT 2"; do
	echo >&2 "ClickHouse is unavailable - sleeping"
	sleep 1
done

# Define the array of table names

my_tables=(
	"impressions"
	"impressions_queue"
	"impressions_mv"
	"clicks"
	"clicks_queue"
	"clicks_mv"
	"events"
	"events_queue"
	"events_mv"
	"installs_base"
	"installs_base_mv"
	"attributed_impressions"
	"attributed_clicks"
	"attributed_installs"
	"attribute_clicks_mv"
	"attribute_impressions_mv"
	"attribute_installs_mv"
	"daily_overview"
	"daily_overview_mv"
	# Uncomment the following lines if needed
	# "daily_overview_impressions_mv"
	# "daily_overview_clicks_mv"
	# "daily_overview_attributed_installs_mv"
)

# Loop through each SQL file in the directory and execute it
for table in "${my_tables[@]}"; do
	echo "Processing table: $table"
	sql_file="$INIT_SQL_DIR/$table.sql"
	if [ -f "$sql_file" ]; then
		echo "Running $sql_file"

		# Check if running in Docker and modify the SQL file content accordingly
		if [ "$ISDOCKER" = true ]; then
			modified_sql=$(sed 's/localhost:9092/kafka:9092/g' "$sql_file")
		else
			modified_sql=$(cat "$sql_file")
		fi

		# Execute setting and SQL file in the same session
		(
			echo "SET allow_experimental_refreshable_materialized_view = 1;"
			echo "$modified_sql"
		) | clickhouse-client -n
	else
		echo "No SQL files found in $INIT_SQL_DIR"
	fi
done

echo >&2 "ClickHouse tables have been initialized"
