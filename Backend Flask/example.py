from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time
import json
import requests
from bs4 import BeautifulSoup
import random

def initialize_browser():
    chrome_options = Options()
    # Fix 1: Specify the version_main parameter
    driver = uc.Chrome(version_main=134, options=chrome_options)
    return driver

def navigate_to_url(driver, url):
    driver.get(url)
    print(f"Navigated to {url}")
    time.sleep(3)  # Allow page to load
    return driver

def fill_input_form(driver, class_name, text, wait_time=10):
    try:
        print(f"Looking for element with class: {class_name}")
        wait = WebDriverWait(driver, wait_time)
        
        # Fix 2: Use correct parameters for find_element
        input_form = wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        print(f"Found form with class: {class_name}")
        
        # Fix 3: Correct the find_element syntax - it doesn't take a tuple
        input_field = input_form.find_element(By.ID, "q")  # "q" is typically the ID for search boxes
        
        input_field.clear()
        for char in text:
            input_field.send_keys(char)
            # Small random delay between keystrokes to appear more human-like
            time.sleep(0.05)
            
        print(f"Entered text: '{text}' into form {class_name}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def click_button_by_class(driver, class_name, wait_time=10):
    try:
        print(f"Looking for element with class: {class_name}")
        # Wait for the button to be clickable
        wait = WebDriverWait(driver, wait_time)
        
        # Fix 4: Remove the dot from the class name parameter
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary")))
        
        # Click the button
        button.click()
        print(f"Successfully clicked the button with class='{class_name}'")
        # Wait a moment to see the result (optional)
        time.sleep(2)
        
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def scrape_lyrics(url):
    headers = {"User-Agent": "Mozilla/5.0"}   
    response = requests.get(url, headers=headers).text
    # Add a random delay (3-7 seconds) to avoid bot detection
    delay = random.uniform(3, 7)
    print(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)
    soup = BeautifulSoup(response, 'lxml')
    topPanel = soup.find('div', class_='panel-heading')
    panelText = topPanel.small.text.replace(' ', '')
    NumberOfResults = panelText[3]
    print(NumberOfResults)

    songResults = []
    songs = soup.findAll('td', class_='text-left visitedlyr')
    for i in range(int(NumberOfResults)):
        songResult = {}
        songResult['song_name'] = songs[i].text.strip()
        songResult['song_url'] = songs[i].a['href']
        print(f"{i+1}. {songResult['song_name']} - {songResult['song_url']}")
        songResults.append(songResult)
    
    # Save the results to JSON
    json_filename = "./resultsFound.json"
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(songResults, file)

    print("Song results saved to resultsFound.json!")

    for song in songResults:
        song_name = song["song_name"]
        song_url = song["song_url"]

        print(f"Fetching lyrics for: {song_name} ...")

        # Add a random delay (3-7 seconds) to avoid bot detection
        delay = random.uniform(3, 7)
        print(f"Waiting for {delay:.2f} seconds...")
        time.sleep(delay)

        # Get lyrics and store them in JSON
        song["lyrics"] = extract_lyrics(song_url)

    # Save updated JSON file with lyrics
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(songResults, file, indent=4)

    print("All lyrics saved!")

def extract_lyrics(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url} (HTTP {response.status_code})")
        return "Failed to fetch."
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first <b> tag (song title)
    song_title = soup.find("b")
    if not song_title:
        return "Song title not found."
    
    # Find first two consecutive <br> tags
    br_count = 0
    next_element = song_title

    while next_element:
        next_element = next_element.find_next()
        if next_element and next_element.name == "br":
            br_count += 1
        else:
            br_count = 0  # Reset if non-<br> element is found

        # Stop when two consecutive <br> tags are found
        if br_count == 2:
            break

    lyrics_div = next_element.find_next("div") if next_element else None

    if lyrics_div:
        # Extract lyrics while preserving line breaks
        lyrics = "<br>".join([line.strip() for line in lyrics_div.stripped_strings])
        return lyrics
    else:
        return "Lyrics not found."

if __name__ == "__main__":
    # Initialize the browser
    driver = initialize_browser()
    
    try: 
        # Navigate to website
        navigate_to_url(driver, "https://www.azlyrics.com/")
        
        # Fix 5: Add the search text parameter
        text = input("Please enter the songname: ")
        time.sleep(5)
        fill_input_form(driver, "search", text)
        
        # Click on a button
        click_button_by_class(driver, "btn-primary")

        time.sleep(3)
        newUrl = driver.current_url
        print(f"current url: {newUrl}")

        scrape_lyrics(newUrl)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Always close the browser when done
        try:
            driver.quit()
        except:
            pass