import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os.path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def getData(filename):
    input = open(filename, "r") 
    data = input.read()
    data_into_list = data.replace('\n', ' ').split(", ")
    return data_into_list

def scrape_phrases(word):
    print(word)
    URL = f"https://www.rhymezone.com/r/rhyme.cgi?Word={word}&typeofrhyme=phr&org1=syl&org2=l&org3=y"
    driver.get(URL)
    similarwords_div = driver.find_element(By.ID, "similarwords")
    similarwords_trs = similarwords_div.find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    similarwords = []
    for tr in similarwords_trs:
        similarwords.extend([td.find_element(By.TAG_NAME, "a").text for td in tr.find_elements(By.TAG_NAME, "td")])
    similarphrases = [phrase.replace(word.lower(), '') for phrase in similarwords if not phrase == word]
    wikiwords_div = driver.find_element(By.ID, "wikiwords")
    wikiwords_trs = wikiwords_div.find_element(By.TAG_NAME, 'center').find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    wikiwords = []
    for tr in wikiwords_trs:
        wikiwords.extend([td.find_element(By.TAG_NAME, "a").text for td in tr.find_elements(By.TAG_NAME, "td")])
    wikiphrases = [phrase.replace(word, '') for phrase in wikiwords if not phrase == word]
    phrases = similarphrases + wikiphrases
    common_phrases = ['', ' (disambiguation)', ' (film)', ' (given name)', ' (surname)', ' (album)', ' ', ' (band)', ' (singer)', ' (rapper)', ' (song)', ' (software)', ' (TV series)', 'the', 'The']
    phrases = [phrase for phrase in phrases if phrase not in common_phrases]
    return list(set(phrases))

def add_phrases_to_dict(word):
    for phrase in scrape_phrases(word):
        if phrase in phrase_dict:
            phrase_dict[phrase].append(word)
        else:
            phrase_dict[phrase] = [word]

def generate_phrase_dict(file):
    for word in getData(file):
        add_phrases_to_dict(word)
    res = [(n, k, v) for n, v, k in sorted(zip(map(len, phrase_dict.values()), phrase_dict.values(), phrase_dict.keys()), reverse=True)]
    res = [phrase for phrase in res if phrase[0] > 1]
    return res


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
homedir = os.path.expanduser("~")
chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
chrome_options.add_argument("--headless=new")
webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")
print("script running")
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
print("driver started")
phrase_dict = {}
sorted_phrase_dict = generate_phrase_dict('input2.txt')
print(*sorted_phrase_dict, sep='\n')