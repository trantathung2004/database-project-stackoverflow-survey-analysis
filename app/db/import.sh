#!/bin/bash

source .env
USER="$MYSQL_USER"
DB="$MYSQL_DB"
PASSWORD="$MYSQL_PASSWORD" 

for file in cleaned-data/*.csv; do
  table=$(basename "$file" .csv)
  abs_path=$(realpath "$file")
  
  echo "Importing $abs_path into table $table..."

  mysql --local-infile=1 -u"$USER" -p"$PASSWORD" "$DB" -e "
    LOAD DATA LOCAL INFILE '$abs_path'
    INTO TABLE $table
    FIELDS TERMINATED BY ','
    ENCLOSED BY '\"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;"
done