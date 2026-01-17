#!/bin/bash

# Run tests (don't exit on test failure)
pytest --alluredir=/app/allure-results -v || true
TEST_EXIT_CODE=${PIPESTATUS[0]}

echo "Tests completed. Generating Allure report..."
sleep 2

# Generate Allure report using default project
curl -sf "http://allure:5050/allure-docker-service/generate-report" && echo "Allure report generated successfully!" || echo "Warning: Could not generate Allure report"

exit $TEST_EXIT_CODE
