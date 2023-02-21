import os

SEASONS = list(range(2016, 2023))

DATA_DIR = 'data'
SCHEDULE_DIR = os.path.join(DATA_DIR, 'schedule')
SCORES_DIR = os.path.join(DATA_DIR, 'scores')

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time




def get_html(url, selector, sleep = 4 , retries = 3):
    html = None
    for i in range(1, retries + 1):
        time.sleep(sleep * i)
        try:
            with sync_playwright() as p:
                browser = p.firefox.launch()
                page = browser.new_page()
                page.goto(url)
                print(page.title())
                html = page.inner_html(selector)
        except PlaywrightTimeout:
            print(f'Timeout error on {url}')
            continue
        else:
            break
    return html 

def scrape_season(season):
    url = f'https://www.basketball-reference.com/leagues/NBA_{season}_games.html'
    html = get_html(url, '#content .filter')

    soup = BeautifulSoup(html)
    links = soup.find_all('a')
    schedule_pages = [f"https://www.basketball-reference.com{l['href']}" for l in links]

    for url in schedule_pages:
        save_path = os.path.join(SCHEDULE_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = get_html(url, "#all_schedule")
        with open(save_path, 'w+', encoding = 'utf-8') as f:
            f.write(html)

#for season in SEASONS:
#    scrape_season(season)

schedule_files = os.listdir(SCHEDULE_DIR)

def scrape_game(schedule_file):
    with open(schedule_file, 'r', encoding = 'utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, features= 'html5lib')
    links = soup.find_all('a')
    hrefs = [l.get('href') for l in links]
    box_scores = [f"https://www.basketball-reference.com{l}" for l in hrefs if l and "boxscore" in l and '.html' in l]

    for url in box_scores:
        save_path = os.path.join(SCORES_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = get_html(url, "#content")
        if not html:
            continue 
        with open(save_path, "w+", encoding = 'utf-8') as f:
            f.write(html)



for game in schedule_files:
    filepath = os.path.join(SCHEDULE_DIR, game)
    scrape_game(filepath)


