#!/bin/bash

source .env
USER="$MYSQL_USER"
DB="$MYSQL_DB"
PASSWORD="$MYSQL_PASSWORD" 

for file in app/db/cleaned-data/*.csv; do
  table=$(basename "$file" .csv)
  echo "Importing $file into table $table..."
  
  # Convert Windows path to MySQL compatible path
  file_path=$(cygpath -w "$(pwd)/$file" | sed 's/\\/\\\\/g')
  
  mysql --local-infile=1 -u "$USER" -p "$DB" -e "
    LOAD DATA LOCAL INFILE '$file_path'
    INTO TABLE $table
    FIELDS TERMINATED BY ','
    ENCLOSED BY '\"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 ROWS;"
done