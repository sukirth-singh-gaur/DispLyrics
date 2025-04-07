from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
CORS(app)
def initialize_browser():
    options = Options()
    options.add_argument("--headless")
    driver = uc.Chrome(version_main=134, options=options)
    return driver

def extract_lyrics(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to fetch."

    soup = BeautifulSoup(response.text, "html.parser")
    song_title = soup.find("b")
    if not song_title:
        return "Song title not found."

    br_count = 0
    next_element = song_title

    while next_element:
        next_element = next_element.find_next()
        if next_element and next_element.name == "br":
            br_count += 1
        else:
            br_count = 0
        if br_count == 2:
            break

    lyrics_div = next_element.find_next("div") if next_element else None
    if lyrics_div:
        lyrics = "<br>".join([line.strip() for line in lyrics_div.stripped_strings])
        return lyrics
    else:
        return "Lyrics not found."

@app.route("/get_lyrics", methods=["GET"])
def get_lyrics():
    song_name = request.args.get("song")
    if not song_name:
        return jsonify({"error": "Missing song name"}), 400

    driver = initialize_browser()
    try:
        driver.get("https://www.azlyrics.com/")
        time.sleep(2)

        wait = WebDriverWait(driver, 10)
        search_form = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search")))
        input_field = search_form.find_element(By.ID, "q")
        input_field.send_keys(song_name)
        time.sleep(1)

        button = driver.find_element(By.CLASS_NAME, "btn-primary")
        button.click()
        time.sleep(3)

        current_url = driver.current_url
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        songs = soup.findAll('td', class_='text-left visitedlyr')

        if not songs:
            return jsonify({"error": "No songs found"}), 404

        first_song_url = songs[0].a['href']
        lyrics = extract_lyrics(first_song_url)

        return jsonify({
            "song": songs[0].text.strip(),
            "lyrics": lyrics
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    app.run(debug=True)
