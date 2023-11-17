# Imports for scraping RT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests

# Imports for data formatting
import uuid
import hashlib
import json
from datetime import datetime, date


def generate_soup_json(author, text, summary, date_created, source_url):
    TODAY = date.today().strftime("%Y-%m-%d")
    """
    Generate a JSON representation of a document with author and content information.

    Parameters:
    document was created (formatted as "%Y %m, %d").
    source_url (str): The source url of the document

    Returns:
    dict: A dictionary representing the document in JSON format with various attributes.
    """
    output = {}
    # get doc id
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    output['documentID'] = str(uuid.UUID(m.hexdigest()))

    # get authorID
    m = hashlib.md5()
    m.update(author.encode('utf-8'))
    output['authorIDs'] = [str(uuid.UUID(m.hexdigest()))]

    output['fullText'] = text
    # output["spanAttribution"] = [{"authorID":output['authorIDs'][0],
    #                                 "start":0,
    #                                 "end":len(text)}]
    # output["lengthWords"] = len(text.split(' '))
    output["isNeedle"] = False
    output["collectionNum"] = "HRS 1"
    output["source"] = source_url
    output["dateCollected"] = TODAY
    output["dateCreated"] = date_created
    output["publiclyAvailable"] = True
    output["deidentified"] = True
    output["languages"] = ["en"]
    output["sourceSpecific"] = {
        "authorName": author,
        "rtSummary": summary,
    }
    return output


def get_soup(url):
    try:
        time.sleep(1)
        response = requests.get(url)
        if response.url[-5:] == url[-5:]:
            soup = BeautifulSoup(response.text, 'html.parser')
            soup = str(soup).replace('"', '\\"')
            return soup
        return ""
    except:
        # print("request failed for url: " + url)
        return ""


def scrape_reviews(source):
    """
    Scrapes reviews given the name of a source domain into a JSON file.

    Args:
    source(str): id number of the source
e
    Returns:
    list: Returns a list of scraped review JSONs.

    """
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--remote-debugging-port=9222")
    path = "/home/mjjiang/sadiri/rt-scraping/scraping/chromedriver"
    driver = webdriver.Chrome(executable_path=path, options=options)
    # Define and open the target URL
    page_url = f'https://www.rottentomatoes.com/critics/source/{source}'
    driver.get(page_url)
    click_count = 0

    review_count = 0
    review_lens = []
    urls = set()
    next_wait = WebDriverWait(driver, 4)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table', {'data-qa': 'critic-reviews-table'})
    while True:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', {'data-qa': 'critic-reviews-table'})
        # extract reviews section from each page
        with open("/shared/3/projects/hiatus/rotten_tomatoes/raw_output/allsoups.jsonl", 'a') as corpus:
            if table:
                # Find all rows in the table's tbody
                rows = table.find('tbody').find_all('tr', {'data-qa': 'row'})
                # Iterate through the rows to extract the review text
                for row in rows:
                    # Find the review's td element
                    review_td = row.find('td', {'data-qa': 'critic-review'})
                    # find the critic's td element
                    critic_td = row.find(
                        'td', {'data-qa': 'critic-review-title'}).find_next_sibling('td')
                    # Check if the review_td is found
                    if review_td:
                        # Extract the review text
                        date_created = datetime.strptime(review_td.find(
                            'div').find('span').text.strip(), "%b %d, %Y")
                        rt_summary = review_td.find('span').text.strip()
                        review_url = review_td.find(
                            'a', class_="publication-link")['href']
                        if date_created < datetime(2021, 1, 1) and len(review_url) > 0 and review_url not in urls:
                            urls.add(review_url)
                            soup = get_soup(review_url)
                            if soup != "":
                                critic_name = critic_td.find(
                                    'a')['href'].split('/')[-2]
                                review = generate_soup_json(
                                    critic_name,
                                    soup,
                                    rt_summary,
                                    date_created.strftime("%Y-%m-%d"),
                                    review_url
                                )
                                corpus.write(json.dumps(review) + '\n')
                                review_count += 1
            try:
                if(review_count > 0):
                    review_lens.append(review_count)
                next_button = next_wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'rt-button.next'))
                )
                next_button.click()
                click_count += 1
                time.sleep(2.5)
            except Exception as e:
                break

    # Close the WebDriver when done
    driver.quit()
    print("reviews found for source " + str(source) + ": " + str(review_count))
    return


def get_reviews(sources):
    for source in sources:
        scrape_reviews(source)


if __name__ == '__main__':
    get_reviews(range(19, 1001))


# review_jsons = get_reviews(sources)
# with open("/shared/3/projects/hiatus/rotten_tomatoes/raw_output/reviewsoups.jsonl", 'w') as corpus:
#     for i in range(len(review_jsons)):
#         rl = review_jsons[i]
#         for review in rl:
#             corpus.write(json.dumps(review) + '\n')
