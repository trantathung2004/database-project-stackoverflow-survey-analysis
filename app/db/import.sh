#!/bin/bash

USER="root"
DB="db_project"
PASSWORD=""  # or leave blank to be prompted

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