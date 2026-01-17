#!/bin/bash

# =============================================================================
# Test Runner Script for QA Automation Case Study
# =============================================================================
# This script orchestrates the test execution with Docker Compose
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
BROWSER="${UI_TEST_DRIVER_TYPE:-chrome}"
RUN_UI_TESTS=false
RUN_API_TESTS=false
RUN_ALL=false
CLEANUP=false

# Print usage
usage() {
    echo -e "${BLUE}Usage:${NC} $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --ui              Run UI tests only"
    echo "  --api             Run API tests only"
    echo "  --all             Run all tests (UI + API)"
    echo "  --browser <type>  Browser type: chrome or firefox (default: chrome)"
    echo "  --cleanup         Clean up containers after tests"
    echo "  --start-infra     Start only infrastructure (Selenium Grid, MinIO, Allure)"
    echo "  --stop            Stop all containers"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --ui --browser chrome"
    echo "  $0 --api"
    echo "  $0 --all --browser firefox --cleanup"
    echo "  $0 --start-infra"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --ui)
            RUN_UI_TESTS=true
            shift
            ;;
        --api)
            RUN_API_TESTS=true
            shift
            ;;
        --all)
            RUN_ALL=true
            shift
            ;;
        --browser)
            BROWSER="$2"
            shift 2
            ;;
        --cleanup)
            CLEANUP=true
            shift
            ;;
        --start-infra)
            echo -e "${BLUE}Starting infrastructure...${NC}"
            docker compose up -d selenium-hub chrome firefox chrome_video firefox_video minio create-bucket allure allure-ui
            echo -e "${GREEN}Infrastructure started!${NC}"
            echo ""
            echo -e "Selenium Grid:    ${YELLOW}http://localhost:4444${NC}"
            echo -e "Chrome noVNC:     ${YELLOW}http://localhost:7900${NC}"
            echo -e "Firefox noVNC:    ${YELLOW}http://localhost:7901${NC}"
            echo -e "MinIO Console:    ${YELLOW}http://localhost:9001${NC} (minio/minio123)"
            echo -e "Allure Report:    ${YELLOW}http://localhost:5252${NC}"
            exit 0
            ;;
        --stop)
            echo -e "${BLUE}Stopping all containers...${NC}"
            docker compose --profile test down
            echo -e "${GREEN}All containers stopped.${NC}"
            exit 0
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Set RUN_ALL if both or neither specified
if $RUN_ALL; then
    RUN_UI_TESTS=true
    RUN_API_TESTS=true
fi

if ! $RUN_UI_TESTS && ! $RUN_API_TESTS; then
    echo -e "${RED}Error: Please specify --ui, --api, or --all${NC}"
    usage
fi

# Export browser type
export UI_TEST_DRIVER_TYPE=$BROWSER

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}     QA Automation Test Runner${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Clean up previous results
echo -e "${YELLOW}Cleaning up previous test results...${NC}"
rm -rf allure-results/ui-test/* allure-results/api-test/*
mkdir -p allure-results/ui-test allure-results/api-test

# Start infrastructure
echo -e "${YELLOW}Starting infrastructure...${NC}"
docker compose up -d selenium-hub chrome firefox chrome_video firefox_video minio create-bucket allure allure-ui

# Wait for Selenium Grid to be ready
echo -e "${YELLOW}Waiting for Selenium Grid to be ready...${NC}"
until curl -s http://localhost:4444/wd/hub/status | grep -q '"ready": true'; do
    sleep 2
done
echo -e "${GREEN}Selenium Grid is ready!${NC}"

# Run UI Tests
if $RUN_UI_TESTS; then
    echo ""
    echo -e "${BLUE}Running UI Tests with ${BROWSER}...${NC}"
    echo -e "${YELLOW}Watch live: http://localhost:7900 (Chrome) or http://localhost:7901 (Firefox)${NC}"
    docker compose --profile test up ui-test --build || true
fi

# Run API Tests
if $RUN_API_TESTS; then
    echo ""
    echo -e "${BLUE}Running API Tests...${NC}"
    docker compose --profile test up api-test --build || true
fi

# Note: Allure reports are generated inside test containers via run-tests.sh

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}     Tests Completed!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "View Results:"
echo -e "  Allure UI:        ${YELLOW}http://localhost:5252${NC}"
echo -e "  Allure Report:    ${YELLOW}http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html${NC}"
echo -e "  Selenium Grid:    ${YELLOW}http://localhost:4444${NC}"
echo -e "  MinIO Console:    ${YELLOW}http://localhost:9001${NC}"
echo -e "  Test Videos:      ${YELLOW}http://localhost:9000/videos${NC}"
echo ""

# Cleanup if requested
if $CLEANUP; then
    echo -e "${YELLOW}Cleaning up containers...${NC}"
    docker compose --profile test down
    echo -e "${GREEN}Cleanup complete.${NC}"
fi
