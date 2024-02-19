#!/bin/bash

# NOTE: This currently is ONLY for superset run from docker

# Define variables
CONTAINER_NAME="superset_app"
DATASOURCES_FILE="mydatasources.zip"
DASHBOARDS_FILE="mydashboards.zip"
LOCAL_EXPORT_DIR_PATH="./apps/superset/exported/"

export_and_copy() {
	local file=$1
	local export_cmd=$2
	echo "Starting export of $file..."

	if docker exec -it "$CONTAINER_NAME" sh -c "$export_cmd -f '$file'"; then
		echo "Export successful. Copying $file..."
		if docker cp "$CONTAINER_NAME:/app/$file" "$LOCAL_EXPORT_DIR_PATH/$file"; then
			echo "Copy successful."
		else
			echo "Failed to copy $file from Docker container."
			exit 1
		fi
	else
		echo "Failed to export $file."
		exit 1
	fi
}

# Main execution
# export_and_copy "$DATASOURCES_FILE" "superset export_datasources"
export_and_copy "$DASHBOARDS_FILE" "superset export_dashboards"
