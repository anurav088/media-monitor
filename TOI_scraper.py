#Iterates through article's paras 

import csv
import requests
from bs4 import BeautifulSoup

def fetch_and_parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_="_s30J clearfix")
        
        all_text = []
        for element in elements:
            text = element.get_text(separator=' ', strip=True)
            if len(text) > 1200:  # If text exceeds approx 1200 characters, limit it.
                text = text[:1200]  # Trim text to roughly three paragraphs.
            all_text.append(text)
            if len(' '.join(all_text)) >= 1200:
                break  # Stop collecting after approx 1200 characters.

        return ' '.join(all_text)
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage from {url}: {e}")
        return ""

def process_links(csv_input, csv_output):
    with open(csv_input, mode='r', newline='', encoding='utf-8') as infile, \
         open(csv_output, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        
        # Debug: Print headers found in the input CSV
        print(f"Headers in {csv_input}: {reader.fieldnames}")
        
        if reader.fieldnames is None or 'URL' not in reader.fieldnames:
            print("ERROR: CSV FILE DOES NOT HAVE PROPER HEADERS OR 'URL' COLUMN IS MISSING.")
            return
        
        writer = csv.DictWriter(outfile, fieldnames=['Title', 'Date', 'Text'])
        writer.writeheader()
        
        processed_count = 0
        for row in reader:
            if 'URL' in row:
                text = fetch_and_parse(row['URL'])
                writer.writerow({'Title': row['Title'], 'Date': row['Date'], 'Text': text})
                processed_count += 1
                if processed_count % 1000 == 0:
                    print(f"PROCESSED {processed_count} ARTICLES.")

                print(f"Done: {row['Title']}.")
            else:
                print("ERROR: NO URL FOUND FOR THE ENTRY.")


input_csv = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\csv files"
output_csv = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\corpcompoutput.csv"
process_links(input_csv, output_csv)
