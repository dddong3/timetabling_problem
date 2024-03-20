#!/usr/bin/env bash

set -euxo pipefail

FWDIR="$(cd "$(dirname "$0")"; pwd)"
cd "$FWDIR"
cd ../

# Check code format
isort src/ --check
black src/ --check --preview
# Check lint: Not checking the code in website
# flake8 db_scanner/ --exclude **/migrations/
# Check static typing for Python

set +euxo pipefail
