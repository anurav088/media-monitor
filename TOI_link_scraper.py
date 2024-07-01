import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import os

def extract_data(date, starttime, output_directory):
    '''This is a base URL. You can enter an initial date and an end date, and vide the correct starttime.
    The code will run for every date until the end date.
    '''
    base_url = "https://timesofindia.indiatimes.com/{year}/{month}/{day}/archivelist/year-{year},month-{month},starttime-{starttime}.cms"
    url = base_url.format(year=date.year, month=date.month, day=date.day, starttime=starttime)
        
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})  
    data = []
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='UTF-8') 
    rows = soup.find("tr", class_="rightColWrap")
    if not rows:
        print(f"No data found for {date} with starttime {starttime}")
        return
    for row in rows:
        for link in row.find_all('a'):
            href = link.get('href')
            title = link.text.strip()  
            if href and title:
                data.append({'URL': href, 'Title': title})

    filename = os.path.join(output_directory, f'TOI_data_{date.strftime("%Y%m%d")}_{starttime}.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['URL', 'Title'])
        writer.writeheader()
        writer.writerows(data)    
    print(f"Data extracted for {date} with starttime {starttime}. Saved to {filename}")

# Define your desired output directory here
output_directory = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\2023"

# Ensure the directory exists, or create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

start_date = datetime(2023, 11, 1)
end_date = datetime(2023, 12, 31)
time = end_date - start_date

'''THE START_STARTTIME VARIABLE BELOW WILL DIFFER FOR DIFFERENT INITIAL DATES, the value below will only give me the code 
starting from 1/8/2001, so for a different initial date, refer to the starttime in the URL of that date's TOI Archive.
The start time in every url increases 1 by every day, so we are simply using a starttime=+1 in every loop for every date.
'''
start_starttime = 37104
end_starttime = time.days + 37104

for days_offset in range((end_date - start_date).days + 1):
    current_date = start_date + timedelta(days=days_offset)
    for starttime in range(start_starttime, end_starttime):
        extract_data(current_date, starttime, output_directory)

print("Script has completed running.")
