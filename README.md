# DispLyrics
## Tools Used
### Manifest-Chrome Dev Tools, Selenium, BeautifulSoup4, Flask, JavaScript, HTML, CSS, DOM
## Working
### A chrome extension which scrapes the lyrics of the currently playing song from AZ-Lyrics.com using Selenium and BeautifulSoup4.    
### The python scraping script is made into a Flask app.  
### The chrome extension sends a GET request to the Flask server with the song name and the server responds back with the song's lyrics.  
### Rest of the UI on the Spotify webpage like enabling the Lyrics Button for songs with lyrics not available and getting the currently playing song is done using DOM manupulations.  
### Appropriate CSS styling is done to fit the Spotify Theme.  
### Popup page is developed so that users can get logs of whether the backend is working or not.  

## Sample
![Description](assets/images/Screenshot%202025-04-27%20230235.png)



# DispLyrics API (Docker + Selenium)

A **local-only HTTP API** that fetches song lyrics using a real browser session (Chromium + Selenium), packaged in Docker.

This project is designed to be used as:

* a **personal lyrics backend**
* a **browser extension API**
* an **educational example** of browser-based scraping

>  This is **not** a hosted service and **must not** be deployed publicly.



## Overview

This application exposes a simple HTTP endpoint that:

1. Accepts a song name
2. Searches for the song using a real browser session
3. Navigates to the lyrics page
4. Extracts and returns lyrics as structured text

Because it uses a **real browser (Selenium)** instead of raw HTTP requests, it can handle sites that block traditional scraping.



## API Specification

### Base URL

```
http://localhost:5001
```



### GET `/get_lyrics`

Fetch lyrics for a given song.

#### Query Parameters

| Name   | Type   | Required | Description             |
| ------ | ------ | -------- | ----------------------- |
| `song` | string |  yes    | Song name to search for |



#### Example Request

```bash
curl "http://localhost:5001/get_lyrics?song=believer"
```



#### Example Success Response

```json
{
  "song": "1. \"Believer\" - Imagine Dragons",
  "lyrics": "First things first\nI'ma say all the words inside my head\n..."
}
```



#### Example Error Responses

```json
{ "error": "Missing song name" }
```

```json
{ "error": "No songs found" }
```

```json
{ "error": "Lyrics not found" }
```



## Architecture (API-centric)

```
Client (curl / browser / extension)
        |
        | HTTP GET /get_lyrics
        v
Flask API (Docker)
        |
        | Selenium (Chromium)
        v
Target website (real browser session)
        |
        v
HTML → BeautifulSoup → Lyrics extraction
```

### Why Selenium?

Many lyrics websites:

* block `requests` / raw HTTP scraping
* serve bot-detection pages
* require real browser behavior

This API intentionally uses a **full browser session** to ensure reliability.



## Running Locally (Required)

### Prerequisites

* Docker
* Internet connection



### Build the image

```bash
docker build -t lyrics-api .
```



### Run the container

```bash
docker run -p 5001:5000 lyrics-api
```

The API will be available at:

```
http://localhost:5001
```



## Intended Usage

  Personal projects
  Browser extensions
  Local automation
  Educational scraping reference



## Not Intended For

  Public deployment
  Commercial usage
  High-frequency scraping
  Hosting lyrics as a service



## Important Disclaimer

 **Read carefully**

This project:

* Does **not** host or redistribute lyrics
* Fetches content dynamically using the user’s own browser session
* Is provided for **educational and personal use only**

All lyrics and content belong to their respective copyright holders.

Users are responsible for complying with the terms of service of any website accessed using this software.

**Do not deploy this as a public API.**



## Performance Notes

* Each request launches browser navigation → expect **3–6 seconds latency**
* Repeated requests may trigger anti-bot protections
* Caching and rate-limiting are strongly recommended for extended use



## Future Improvements (Optional)

* In-memory or persistent caching
* Reusing Selenium sessions
* Extension-specific optimizations



## License

This project is provided under the **MIT License**
(usage responsibility remains with the user).


