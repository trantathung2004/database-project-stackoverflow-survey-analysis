#!/bin/bash

# Wait for MySQL to be fully up
echo "Waiting for MySQL to be ready..."
while ! mysqladmin ping -h mysql --silent; do
    sleep 2
done

# Run create_users_csv.py to generate Users.csv with admin account
echo "Creating Users.csv with admin account..."
python db/data_users.py
source ./path/to/.env

# Import CSV files into corresponding tables
CLEANED_DATA_DIR="app/db/cleaned-data"
MYSQL_USER="$MYSQL_USER"
MYSQL_PASSWORD="$MYSQL_PASSWORD"
MYSQL_DATABASE="$MYSQL_DATABASE"
MYSQL_HOST="$MYSQL_HOST"
echo "MYSQL_HOST=$MYSQL_HOST"
echo "MYSQL_USER=$MYSQL_USER"
echo "MYSQL_PASSWORD=$MYSQL_PASSWORD"
echo "MYSQL_DATABASE=$MYSQL_DATABASE"
for csv_file in $CLEANED_DATA_DIR/*.csv; do
    if [ -f "$csv_file" ]; then
        # Extract table name from CSV filename (e.g., Users.csv -> accounts)
        table_name=$(basename "$csv_file" .csv)
        # Map Users.csv to accounts table
        echo "Importing $csv_file into table $table_name..."

        # Get the header row to determine columns
        columns=$(head -n 1 "$csv_file" | tr -d '\n' | tr -d '\r')

        # Create LOAD DATA query
        mysql --local-infile=1 -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e \
            "LOAD DATA LOCAL INFILE '$csv_file' INTO TABLE $table_name \
            FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' \
            IGNORE 1 LINES ($columns);"

        if [ $? -eq 0 ]; then
            echo "Successfully imported $csv_file into $table_name"
        else
            echo "Error importing $csv_file"
        fi
    fi
done

echo "CSV import completed."