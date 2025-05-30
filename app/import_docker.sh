#!/bin/bash

# Wait for MySQL to be fully up
echo "Waiting for MySQL to be ready..."
while ! mysqladmin ping -h mysql --silent; do
    sleep 2
done
ls
# Run create_users_csv.py to generate Users.csv with admin account
echo "Creating Users.csv with admin account..."
python3 db/data_users.py
source .env

# Import CSV files into corresponding tables
CLEANED_DATA_DIR="db/cleaned-data"
MYSQL_USER="$MYSQL_USER"
MYSQL_PASSWORD="$MYSQL_ROOT_PASSWORD"
MYSQL_DATABASE="$MYSQL_DATABASE"
MYSQL_HOST="$MYSQL_HOST"
MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD"

set -e  # exit on error
mysql -u root -p"${MYSQL_PASSWORD}"<<-EOSQL
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOSQL

MYSQL_CMD="mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE"

echo "Running create tables scripts..."
$MYSQL_CMD < db/database-init/create-tables.sql
echo ${MYSQL_ROOT_PASS}


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
echo "Running other SQL scripts..."
$MYSQL_CMD < db/database-init/set-constraints.sql
$MYSQL_CMD < db/database-init/create-views.sql
$MYSQL_CMD < db/database-init/create-indexes.sql
$MYSQL_CMD < db/database-init/create-procedures.sql
$MYSQL_CMD < db/database-init/create-triggers.sql
