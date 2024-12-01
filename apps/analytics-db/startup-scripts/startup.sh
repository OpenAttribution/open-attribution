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
)

# Add drop tables section before creating new ones
echo "Dropping existing tables..."
for table in "${my_tables[@]}"; do
	echo "Dropping table: $table"
	clickhouse-client --query "DROP TABLE IF EXISTS $table"
done

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

		# Execute using heredoc syntax
		clickhouse-client -n <<-EOSQL
			SET allow_experimental_refreshable_materialized_view = 1;
			${modified_sql}
		EOSQL
	else
		echo "No SQL files found in $INIT_SQL_DIR"
		exit 1
	fi
done

echo >&2 "ClickHouse tables have been initialized"
