#!/bin/bash

# Exit on error, undefined vars, and pipe failures
set -euo pipefail

echo "🧪 Running tests with verbose output..."
pytest -vvv -s tests/*.py

echo "📊 Generating coverage report..."
pytest --cov=core --cov-report=html tests/*.py

echo "🌐 Opening coverage report..."
if command -v xdg-open &> /dev/null; then
    xdg-open htmlcov/index.html
elif command -v open &> /dev/null; then    # For macOS
    open htmlcov/index.html
else
    echo "⚠️  Could not open coverage report automatically. Please open htmlcov/index.html manually."
fi
