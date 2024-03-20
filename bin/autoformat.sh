#!/usr/bin/env bash

set -euxo pipefail

FWDIR="$(cd "$(dirname "$0")"; pwd)"
cd "$FWDIR"
cd ../

# Autoformat code
isort src/ --profile black
black src/ --preview

isort tests/ --profile black
black tests/ --preview

set +euxo pipefail
