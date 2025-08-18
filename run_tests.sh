#!/bin/bash
# Run pytest and append results to logs/test_log.txt with a timestamp.
set -e
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/test_log.txt"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
if pytest; then
  RESULT="PASS"
else
  RESULT="FAIL"
fi
echo "$TIMESTAMP $RESULT" >> "$LOG_FILE"
[ "$RESULT" = "PASS" ]
