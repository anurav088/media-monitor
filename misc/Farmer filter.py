import csv

# Define the keywords
keywords = ["Farm", "Farmers", "Farmers Protests","Farmer", "Farmers Laws", "MSP", "Agricultural",
    "APMC", "Tractor","crop","Farmer Protest","Agriculture"]

# Convert keywords to lowercase for case-insensitive matching
keywords = [keyword.lower() for keyword in keywords]

def filter_csv(input_filename, output_filename):
    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile, \
        open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

            # Write the header to the output fileh
        headers = next(reader)
        writer.writerow(headers)

        # Process each row in the input file
        for row in reader:
            title = row[2].lower()  # Assuming title is the third column
            if any(keyword in title for keyword in keywords) :
                writer.writerow(row)

# Specify the input and output CSV file names
input_csv = r"C:\Users\Adity\Desktop\Python\Farmers4.csv"  # Change this to your input CSV file name
output_csv = r"C:\Users\Adity\Desktop\Python\FinalFarmerData2.csv"  # Change this to your desired output CSV file name

# Call the function
filter_csv(input_csv, output_csv)

print("Filtering complete. Check the output CSV file.")
