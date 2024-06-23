import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def extract_data(date, starttime):
    '''this is a base url, you can enter an initial date and an end date on line 30, and provide the correct starttime.
    and the code will run it for every date till the end date.
    '''
    base_url = "https://timesofindia.indiatimes.com/{year}/{month}/{day}/archivelist/year-{year},month-{month},starttime-{starttime}.cms"
    url = base_url.format(year=date.year, month=date.month, day=date.day, starttime=starttime)

        
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})  
    data = []
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='UTF-8') 
    #All the article heading title's and links lay in the class tr rightColWrap
    rows= soup.find("tr",class_="rightColWrap")
    for row in rows:
        for link in row.find_all('a'):
            href = link.get('href')
            title = link.text.strip()  
            if href and title:
                data.append({'URL': href, 'Title': title})

    filename = f'TOI_data_{date.strftime("%Y%m%d")}_{starttime}.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['URL', 'Title'])
        writer.writeheader()
        writer.writerows(data)

start_date = datetime(2001, 8, 1)  
end_date = datetime(2001,8 , 5)  
time=end_date-start_date
'''THE START_STARTTIME VARIABLE BELOW WILL DIFFER FOR DIFFERENT INITIAL DATES, the value below will only give me the code 
starting from 1/8/2001, so for a different initial date, refer to the starttime in the URL of that dates TOI Archive.
The start time in every url increases 1 by every day, so we are simply using a starttime=+1 in every loop for every date.
'''
start_starttime = 37104
end_starttime = time.days + 37104 

# hERE WE ARE looping through the days for every starttime(as the starttime in every URL also increases by 1 every day)
for days_offset in range((end_date - start_date).days + 1):
    current_date = start_date + timedelta(days=days_offset)

    for starttime in range(start_starttime, end_starttime): 
        extract_data(current_date, starttime)