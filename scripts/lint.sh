#!/usr/bin/env bash

set -x

status=0

# if ! mypy app; then 
#   status=1
# fi

# if ! black app --check; then 
#   status=1
# fi

# if ! flake8 app; then 
#   status=1
# fi

# if ! isort --check-only app; then 
#   status=1
# fi

exit $status
