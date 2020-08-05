#!/bin/bash -e

CONF=cmms/cmms/mysql.cnf

if ! [ -e "$CONF" ]; then
  cat > "$CONF" << %
[client]
database = ${DB_NAME:-CMMS}
user = ${DB_USER:-cmms}
password = ${DB_PASSWORD:-cmms}
%
fi

cd cmms

if [ "$AUTO_MIGRATE" = "true" ]; then
  python3 manage.py migrate
fi

exec python3 manage.py runserver 0.0.0.0:8000
