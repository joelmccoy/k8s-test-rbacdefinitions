#! /bin/sh
set -ex
pip install -r "/tests/requirements.txt"

set -e
echo "Running tests..."
pytest /tests
export TEST_EXIT_CODE=$?

exit $TEST_EXIT_CODE