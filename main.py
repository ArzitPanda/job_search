from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


def scrape_jobs_from_website(url):
  # Example: Simple web scraping using BeautifulSoup
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  # Extract job information
  job_element = soup.find('ul', id="lcp_instance_0")
  job_list = job_element.find_all('li')

  job_data = []
  for li in job_list:
    link = li.find('a')
    if link:
      url = link.get('href')
      text = link.text.strip()

      print(f"URL: {url}")
      print(f"Text: {text}")
      print("--------------------")
      job_data.append({url: url, text: text})

  return job_data


def scrape_jobs_cse(url):
  # Example: Simple web scraping using BeautifulSoup
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  # Extract job information
  job_element = soup.find('ul',
                          class_=lambda x: x and x.startswith(
                              'SearchResultsstyle__SearchResultsWrapper'))

  # job_element = soup.find(
  #     'ul', class_="SearchResultsstyle__SearchResultsWrapper-sc-c560t5-0")
  job_list = job_element.find_all('li')
  job_data_list = []
  for li in job_list:
    job_title = li.select_one(
        '.JobTeaserstyle__JobTeaserTitleLink-sc-1p2iccb-2')
    company_name = li.select_one('.Logostyle__Title-sc-tecoyk-2')
    location = li.select_one('.JobTeaserstyle__JobLocation-sc-1p2iccb-8')
    job_description = li.select_one(
        '.JobTeaserstyle__JobTeaserOverview-sc-1p2iccb-10')
    application_close_date = li.select_one('.sc-eFubAy.field-item')
    logo_url = li.select_one('.Logostyle__Image-sc-tecoyk-1')

    job_title_text = job_title.text.strip() if job_title else 'N/A'
    company_name_text = company_name.text.strip() if company_name else 'N/A'
    location_text = location.text.strip() if location else 'N/A'
    job_description_text = job_description.text.strip(
    ) if job_description else 'N/A'
    application_close_date_text = application_close_date.text.strip(
    ) if application_close_date else 'N/A'
    logo_url_text = logo_url['src'] if logo_url else 'N/A'
    job_data = {
        'Job Title': job_title_text,
        'Company Name': company_name_text,
        'Location': location_text,
        'Job Description': job_description_text,
        'Application Close Date': application_close_date_text,
        'Logo URL': logo_url_text
    }

    # Append the dictionary to the list

    job_data_list.append(job_data)

  return job_data_list


@app.route('/')
def home():
  return 'Welcome to the Job Scraper API!'


@app.route('/scrape_generic_jobs')
def scrape_generic_jobs():
  url = "https://www.careerpower.in/blog/"
  job_data = scrape_jobs_from_website(url)
  return jsonify(job_data)


@app.route('/scrape_cse_jobs/<int:page>')
def scrape_cse_jobs(page):
  start_page = page * 20
  url = f"https://in.prosple.com/jobs-for-computer-science-engineering-cse-freshers-india?content=jobs-for-computer-science-engineering-cse-freshers-india&start={start_page}"
  job_data = scrape_jobs_cse(url)
  return jsonify(job_data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
