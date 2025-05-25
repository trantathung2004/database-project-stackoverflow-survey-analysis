#!/bin/bash

USER="root"
PASSWORD="root"
DB="db_project"

for file in /docker-entrypoint-initdb.d/cleaned-data/*.csv; do
  table=$(basename "$file" .csv)
  echo "Importing $file into table $table..."
  
  mysql --local-infile=1 -u"$USER" -p"$PASSWORD" "$DB" -e "
    LOAD DATA LOCAL INFILE '$file'
    INTO TABLE $table
    FIELDS TERMINATED BY ','
    ENCLOSED BY '\"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;"
done
