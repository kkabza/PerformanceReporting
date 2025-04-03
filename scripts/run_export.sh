#!/bin/bash
# Script to run CSV export with predefined values and handle errors

# Get API key from environment variable
if [ -z "$GRAFANA_API_KEY" ]; then
    echo "Error: GRAFANA_API_KEY environment variable is not set"
    exit 1
fi

# Calculate yesterday's date in ISO format with 8am and 4pm times
YESTERDAY=$(date -v-1d +"%Y-%m-%d")
FROM_TIME="${YESTERDAY}T08:00:00Z"
TO_TIME="${YESTERDAY}T16:00:00Z"

echo "Exporting data from $FROM_TIME to $TO_TIME"

# Run the export script with detailed debugging
./scripts/export_grafana_csv.py \
  --api-key "$GRAFANA_API_KEY" \
  --output yesterday_8to4.csv \
  --from-time "$FROM_TIME" \
  --to-time "$TO_TIME" \
  --var-aggregation "10" \
  --var-request ".*" \
  --var-transaction ".*" \
  --debug

# Check the exit code
if [ $? -eq 0 ]; then
  echo "✅ CSV export completed successfully!"
  echo "CSV file saved as: yesterday_8to4.csv"
else
  echo "❌ CSV export failed. Check the logs for details."
  echo "See grafana_export.log for complete logs."
fi 