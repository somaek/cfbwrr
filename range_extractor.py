import csv

# Prompt the user for the range of column 1
begin_value = int(input("Enter the beginning value of the range: "))
end_value = int(input("Enter the end value of the range: "))

# Construct the output file name using the user-entered values
output_file_name = f"output_{begin_value}_{end_value}.csv"

# Open the input and output CSV files
with open('calculated_results1901-2022.csv', 'r') as input_file, open(output_file_name, 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate over the rows in the input CSV file
    for row in reader:
        # Check if the value of column 1 falls within the specified range
        if begin_value <= int(row[0]) <= end_value:
            # Write the row to the output CSV file
            writer.writerow(row)