# DispLyrics

![Description](assets/images/Screenshot%202025-04-27%20230235.png)

## The Problem
Spotify’s web player does not provide lyrics for many songs. I built a Chrome extension called DispLyrics that enables the lyrics feature even for songs that don’t officially have lyrics available.
## The Solution
The extension fetches lyrics from AZLyrics using a backend scraping service and dynamically injects them into the Spotify UI.

## Tools & Technologies

* **Frontend:** JavaScript, HTML, CSS, DOM Manipulation
* **Backend:** Python, Flask
* **Scraping:** Selenium, BeautifulSoup4
* **Dev Tools:** Chrome DevTools
* **Containerization:** Docker


# Working

DispLyrics enhances the Spotify web player by enabling the **Lyrics button** for songs that do not have official lyrics available.

When a song is played:

1. The Chrome extension detects the **currently playing track** using DOM inspection on the Spotify webpage.
2. The extension sends a **GET request** to a locally running Flask API with the song name.
3. The Flask backend launches a **Chromium browser session using Selenium**.
4. Selenium navigates to **AZLyrics**, searches for the song, and loads the lyrics page.
5. **BeautifulSoup4** parses the HTML and extracts the lyrics.
6. The API returns the lyrics as JSON.
7. The extension dynamically **injects the lyrics into the Spotify UI** with styling that matches the Spotify theme.

A popup page in the extension shows **backend logs and status** so users can verify whether the API is running.


# DispLyrics API (Docker + Selenium)

A **local-only HTTP API** that fetches song lyrics using a real browser session (Chromium + Selenium), packaged in Docker.

This project can be used as:

* a personal lyrics backend
* a browser extension API
* an educational example of browser-based scraping

⚠️ This is **not a hosted service** and must **not be deployed publicly**.


# Overview

The API exposes a simple endpoint that:

1. Accepts a **song name**
2. Searches for the song using a **real browser session**
3. Navigates to the lyrics page
4. Extracts and returns lyrics as structured text

Because it uses a **real browser (Selenium)** instead of raw HTTP requests, it can bypass many anti-scraping protections used by lyrics websites.


# API Specification

## Base URL

```
http://localhost:5001
```


## GET /get_lyrics

Fetch lyrics for a given song.

### Query Parameters

| Name | Type   | Required | Description             |
| ---- | ------ | -------- | ----------------------- |
| song | string | yes      | Song name to search for |


### Example Request

```
curl "http://localhost:5001/get_lyrics?song=believer"
```


### Example Success Response

```json
{
  "song": "1. \"Believer\" - Imagine Dragons",
  "lyrics": "First things first\nI'ma say all the words inside my head\n..."
}
```


### Example Error Responses

```json
{ "error": "Missing song name" }
```

```json
{ "error": "No songs found" }
```

```json
{ "error": "Lyrics not found" }
```


# Architecture

```
Client (Extension / Browser / curl)
        |
        | HTTP GET /get_lyrics
        v
Flask API (Docker Container)
        |
        | Selenium → Chromium Browser
        v
Target Website (AZLyrics)
        |
        v
HTML → BeautifulSoup → Lyrics Extraction
```


# Why Selenium?

Many lyrics websites:

* block raw HTTP requests
* implement bot detection
* require real browser behavior

Using **Selenium with a real Chromium browser session** improves scraping reliability.


# Running Locally

## Prerequisites

* Docker
* Internet connection


## Build Docker Image

```
docker build -t lyrics-api .
```


## Run Container

```
docker run -p 5001:5000 lyrics-api
```

The API will be available at:

```
http://localhost:5001
```


# Intended Usage

* Personal projects
* Browser extensions
* Local automation
* Educational scraping reference


# Not Intended For

* Public deployment
* Commercial usage
* High-frequency scraping
* Hosting lyrics as a service


# Important Disclaimer

This project:

* Does **not host or redistribute lyrics**
* Fetches content dynamically using the **user’s own browser session**
* Is provided for **educational and personal use only**

All lyrics belong to their respective copyright holders.

Users are responsible for complying with the **terms of service** of any website accessed using this software.

⚠️ Do **not deploy this as a public API**.

# Performance Notes

* Each request launches browser navigation → **3–6 seconds latency**
* Repeated requests may trigger **anti-bot protections**
* **Caching and rate limiting** are recommended for extended use


# Future Improvements

* In-memory or persistent caching
* Reusing Selenium sessions
* Extension-specific optimizations
* Faster scraping using fallback APIs


# License

This project is released under the **MIT License**.



