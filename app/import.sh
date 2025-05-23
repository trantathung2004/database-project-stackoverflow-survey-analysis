#!/bin/bash

USER="root"
DB="db_project"
PASSWORD=""  # or leave blank to be prompted

for file in db/cleaned-data/*.csv; do
  table=$(basename "$file" .csv)
  echo "Importing $file into table $table..."

  mysql --local-infile=1 -u "$USER" -p"$PASSWORD" "$DB" -e "
    LOAD DATA LOCAL INFILE '$(pwd)/$file'
    INTO TABLE $table
    FIELDS TERMINATED BY ','
    ENCLOSED BY '\"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;"
done
