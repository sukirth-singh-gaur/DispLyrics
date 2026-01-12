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

    options.binary_location = "/usr/bin/chromium"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-default-apps")

    driver = uc.Chrome(
        options=options,
        version_main=None,
        driver_executable_path="/usr/bin/chromedriver"
    )

    return driver


def extract_lyrics(driver, url):
    print("\n[DEBUG] Loading lyrics page via Selenium:", url, flush=True)

    driver.get(url)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Find the <b>"Song"</b>
    title_b = soup.find("b", string=lambda s: s and s.strip().startswith('"'))
    if not title_b:
        print("[ERROR] Song title <b> not found (selenium page)", flush=True)
        return "Lyrics not found."

    lyrics_div = title_b.find_next("div")
    if not lyrics_div:
        print("[ERROR] Lyrics div not found", flush=True)
        return "Lyrics not found."

    lyrics = "<br>".join(
        line.strip() for line in lyrics_div.stripped_strings
    )

    print("[SUCCESS] Lyrics extracted via Selenium", flush=True)
    return lyrics




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
        input_field = search_form.find_element(By.CLASS_NAME, "form-control")
        input_field.send_keys(song_name)
        time.sleep(1)

        button = driver.find_element(By.CLASS_NAME, "btn-primary")
        button.click()
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        songs = soup.find_all("td", class_="text-left visitedlyr")


        if not songs:
            return jsonify({"error": "No songs found"}), 404

        first_song_url = songs[0].a['href']
        lyrics = extract_lyrics(driver, first_song_url)

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
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )

