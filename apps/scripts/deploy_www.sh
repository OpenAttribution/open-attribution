#!/bin/bash

# This script is used when deploying the commercial site found at openattribution.dev

cd apps || exit
mkdocs build --site-dir www/static/docs
