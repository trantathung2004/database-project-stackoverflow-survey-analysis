#!/bin/bash

USER="root"
DB="db_project"
PASSWORD="dat231259"  # or leave blank to be prompted

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