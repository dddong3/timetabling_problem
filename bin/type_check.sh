#!/usr/bin/env bash

set -euxo pipefail

FWDIR="$(cd "$(dirname "$0")"; pwd)"
cd "$FWDIR"
cd ../

# Check static typing for Python
mypy --ignore-missing-imports src/

set +euxo pipefail
