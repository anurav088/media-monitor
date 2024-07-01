import csv

# filter using the following defined keywords 
keywords = ["Mergers","Merger","Acquisition","Acquisitions","Takeover", "Takeovers","Antitrust","Monopoly","Consolidation","Competition Commission of India","CCI"]

# Convert keywords to lowercase for case-insensitive matching
keywords = [keyword.lower() for keyword in keywords]

def filter_csv(input_filename, output_filename):
    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile, \
        open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

            # Write the header to the output file
        headers = next(reader)
        writer.writerow(headers)

        # Process each row in the input file
        for row in reader:
            title = row[2].lower()  # Assuming title is the third column
            if any(keyword in title for keyword in keywords) :
                writer.writerow(row)

# Specify the input and output CSV file names   
input_csv = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\corpcomp.csv"  # Change this to your input CSV file name
output_csv = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\corpcomp.csv"  # Change this to your desired output CSV file name

# Call the function
filter_csv(input_csv, output_csv)

print("Filtering complete. Check the output CSV file.")
