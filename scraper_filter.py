# this first filters through articles for keywords before downloading their content - integrating their 
import csv
import requests
from bs4 import BeautifulSoup

# Define the keywords
KEYWORDS = ["Mergers", "Merger", "Acquisition", "Acquisitions", "Takeover", "Takeovers",
            "Antitrust", "Monopoly", "Consolidation", "Competition Commission of India", " CCI "]
KEYWORDS = [keyword.lower() for keyword in KEYWORDS]

def fetch_and_parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_="_s30J clearfix")
        
        all_text = []
        for element in elements:
            text = element.get_text(separator=' ', strip=True)
            if len(text) > 1200:  # Limit text to approx 1200 characters.
                text = text[:1200]  # Trim text.
            all_text.append(text)
            if len(' '.join(all_text)) >= 1200:
                break  # Stop after approx 1200 characters.

        return ' '.join(all_text)
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage from {url}: {e}")
        return ""

def filter_and_process_links(csv_input, csv_output):
    with open(csv_input, mode='r', newline='', encoding='utf-8') as infile, \
         open(csv_output, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        
        print(f"Headers in {csv_input}: {reader.fieldnames}")
        
        if reader.fieldnames is None or 'URL' not in reader.fieldnames or 'Title' not in reader.fieldnames:
            print("ERROR: CSV FILE DOES NOT HAVE PROPER HEADERS OR REQUIRED COLUMNS ARE MISSING.")
            return
        
        writer = csv.DictWriter(outfile, fieldnames=['Title', 'Date', 'Text'])
        writer.writeheader()
        
        processed_count = 0
        for row in reader:
            title = row.get('Title', '').lower()
            if any(keyword in title for keyword in KEYWORDS):
                text = fetch_and_parse(row.get('URL', ''))
                writer.writerow({'Title': row.get('Title', 'N/A'), 
                                 'Date': row.get('Date', 'N/A'),  
                                 'Text': text})
                processed_count += 1
                if processed_count % 1000 == 0:
                    print(f"PROCESSED {processed_count} ARTICLES.")
                
                print(f"Done: {row.get('Title', 'N/A')}.")
            else:
                print(f"Skipped: {row.get('Title', 'N/A')} (No relevant keywords).")

# File paths
input_csv = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\2023\2023_combined.csv"  # Change this to your input CSV file name
output_csv = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\2023_output.csv"  # Change this to yur desired output file name 

filter_and_process_links(input_csv, output_csv)
print("Processing complete. Check the output CSV file.")
