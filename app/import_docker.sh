#!/bin/bash

# Wait for MySQL to be fully up
echo "Waiting for MySQL to be ready..."
while ! mysqladmin ping -h mysql --silent; do
    sleep 2
done

# Run add_admin.py to create admin account
echo "Creating admin account..."
python db/database-init/add_admin.py

# Import CSV files into corresponding tables
CLEANED_DATA_DIR="db/cleaned-data"
MYSQL_USER="user"
MYSQL_PASSWORD="userpassword"
MYSQL_DATABASE="mydb"
MYSQL_HOST="mysql"

for csv_file in $CLEANED_DATA_DIR/*.csv; do
    if [ -f "$csv_file" ]; then
        # Extract table name from CSV filename (e.g., users.csv -> users)
        table_name=$(basename "$csv_file" .csv)
        echo "Importing $csv_file into table $table_name..."

        # Get the header row to determine columns
        columns=$(head -n 1 "$csv_file" | tr -d '\n' | tr -d '\r')

        # Create LOAD DATA query
        mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e \
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

echo "CSV import and admin setup completed."