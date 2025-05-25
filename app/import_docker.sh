#!/bin/bash

echo "Starting CSV data import..."

# Set MySQL connection variables  
MYSQL_CMD="mysql -h localhost -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE"

# Enable local file loading
$MYSQL_CMD -e "SET GLOBAL local_infile = 'ON';"

echo "Importing CSV data..."

# Loop through all CSV files in the directory
for csv_file in /var/lib/mysql-files/*.csv; do
    if [ -f "$csv_file" ]; then
        # Extract filename without path and extension
        filename=$(basename "$csv_file" .csv)
        
        echo "Importing $filename.csv into table $filename..."
        
        # This assumes table name matches CSV filename
        # Adjust the table name logic if needed
        $MYSQL_CMD -e "
        LOAD DATA LOCAL INFILE '$csv_file' 
        INTO TABLE $filename 
        FIELDS TERMINATED BY ',' 
        ENCLOSED BY '\"' 
        LINES TERMINATED BY '\n' 
        IGNORE 1 ROWS;" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "✓ Successfully imported $filename.csv"
        else
            echo "✗ Failed to import $filename.csv"
        fi
    fi
done

echo "CSV import process completed!"

# Show row counts for verification
echo "Verifying imports - Row counts:"
for csv_file in /var/lib/mysql-files/*.csv; do
    if [ -f "$csv_file" ]; then
        filename=$(basename "$csv_file" .csv)
        count=$($MYSQL_CMD -e "SELECT COUNT(*) FROM $filename;" 2>/dev/null | tail -n 1)
        if [ $? -eq 0 ]; then
            echo "$filename: $count rows"
        fi
    fi
done