#!/bin/bash

# NOTE: This currently is ONLY for superset run from docker

# Define variables
CONTAINER_NAME="superset_app"
DATASOURCES_EXPORT_PATH="mydatasources.zip"
DASHBOARDS_EXPORT_PATH="mydashboards.zip"
LOCAL_EXPORT_DIR_PATH="./apps/superset/exported/"

# Function to export from Docker and copy
function export_and_copy {
	local export_path="$1"
	local local_path="$2"
	# local export_name="$(basename "$export_path")"

	echo "Starting export of $export_path..."

	if docker exec "$CONTAINER_NAME" sh -c "superset export_datasources -f '$export_path'"; then
		echo "Export successful. Copying $export_path..."

		# Copy the zip file to the target directory
		if docker cp "$CONTAINER_NAME:$export_path" "$local_path/$export_path"; then
			echo "Copy successful."
		else
			echo "Failed to copy $export_path from Docker container."
			return 1
		fi
	else
		echo "Failed to export $export_path."
		return 1
	fi
}

# Export and Copy Datasources
export_and_copy "$DATASOURCES_EXPORT_PATH" "$LOCAL_EXPORT_DIR_PATH"

# Export and Copy Dashboards
export_and_copy "$DASHBOARDS_EXPORT_PATH" "$LOCAL_EXPORT_DIR_PATH"
