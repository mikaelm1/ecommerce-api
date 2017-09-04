#!/usr/bin/env bash

echo "ls \================================"
ls

# Execute the CMD from the Dockerfile.
exec "$@"