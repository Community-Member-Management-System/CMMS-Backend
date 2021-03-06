#!/bin/bash -e

CONF=cmms/mysql.cnf

if ! [ -e "$CONF" ]; then
  cat > "$CONF" << %
[client]
host = ${DB_HOST:-localhost}
database = ${DB_NAME:-CMMS}
user = ${DB_USER:-cmms}
password = ${DB_PASSWORD:-cmms}
%
fi

if [ "$AUTO_MIGRATE" = "true" ]; then
  python3 manage.py migrate
fi

exec python3 manage.py runserver 0.0.0.0:8000
