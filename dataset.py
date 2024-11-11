import csv
import random

input_csv_filename = 'sudo.csv' # Original dataset that consist of 3 million record. https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings?select=sudoku-3m.csv
output_csv_filename = 'shuffled_sudo2.csv'

num_rows_to_read = 100000

rows = []

# Read CSV file 
with open(input_csv_filename, newline='') as input_file:
    csv_reader = csv.DictReader(input_file)
    for row_num, row in enumerate(csv_reader, start=1):
        if row_num > num_rows_to_read:
            break
        difficulty = float(row['difficulty'])
        if difficulty > 2.5:
            rows.append(row)

random.shuffle(rows)

# Create new CSV file 
with open(output_csv_filename, 'w', newline='') as output_file:
    fieldnames = rows[0].keys()  
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()  
    csv_writer.writerows(rows)  
