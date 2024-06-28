import requests
from bs4 import BeautifulSoup
import csv

def scrape_indeed_jobs(query, location):
    base_url = 'https://www.indeed.com/jobs'
    params = {
        'q': query,
        'l': location
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('div', class_='jobsearch-SerpJobCard'):
        title = job_card.find('h2', class_='title').a.get('title')
        company = job_card.find('span', class_='company').text.strip()
        location = job_card.find('div', class_='location').text.strip()
        summary = job_card.find('div', class_='summary').text.strip()

        jobs.append([title, company, location, summary])

    return jobs

def save_to_csv(jobs, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Location', 'Summary'])
        writer.writerows(jobs)

if __name__ == '__main__':
    query = 'data scientist'
    location = 'San Francisco, CA'
    jobs = scrape_indeed_jobs(query, location)
    save_to_csv(jobs, 'indeed_job_listings.csv')
