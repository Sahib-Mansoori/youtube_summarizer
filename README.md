# 🎬 YouTube Transcript Summarizer with Docker & Firefox

This project automates **fetching YouTube video transcripts** (via Selenium + Firefox) and generates **summaries using an LLM**.
It can process videos directly from URLs or from a channel’s **RSS feed**, then send results to **Telegram**.

Everything runs inside Docker, with a self-contained **Firefox + Geckodriver binary** included.

---

## 🚀 Features

* Extract transcripts from YouTube videos automatically (headless Firefox).
* Summarize transcripts with an LLM.
* Option to process videos manually (URLs) or automatically (RSS feed).
* Telegram integration for sending summaries.
* Dockerized for portability — no need to install Firefox locally.

---

## 📂 Project Structure

```
.
├── app/
│   ├── YT_Summarizer_Final_with_tracking.py    # main entrypoint
│   ├── YT_transcript_multiple.py               # transcript extractor (Selenium)
│   ├── YT_transcript_summarizer.py             # LLM-based summarizer
│   ├── YT_feed_with_tracking_with_limit.py     # RSS feed fetcher + deduplication
│   ├── YT_telegram_message.py                  # Telegram message sender
│   ├── firefox_browser_binary/                 # Firefox binary (downloaded at build time)
│   ├── geckodriver                             # Geckodriver binary (must be placed here)
|   ├── requirements.txt                        # install the python dependencies
│   └── ...
├── transcript_summary/                         # mapped volume for saved transcripts
├── Dockerfile
└── docker-compose.yml
```

---

## 🐳 Setup with Docker

### 1. Build the Docker image

```bash
docker compose build
```

### 2. Run the container

```bash
docker compose run summary_app
```

This will:

* Download **Firefox 142.0.1 (Linux x64)** into `/app/firefox_browser_binary`
* Mount `./transcript_summary` from your host to `/saved` inside the container
* Run the app (`YT_Summarizer_Final_with_tracking.py`)

---

## ⚙️ How It Works

1. **User Input**

   * Enter YouTube URLs (comma-separated)
   * Or type `feed` to process a channel RSS feed

2. **Transcript Extraction**

   * Selenium (Firefox + Geckodriver) scrapes transcripts from YouTube
   * Files are saved under `/saved` (`./transcript_summary` on host)

3. **Summarization**

   * Transcript files are fed into an LLM for summarization
   * Summaries are prepended with the video URL + title

4. **Telegram Delivery**

   * Summaries are split into messages and sent via Telegram
   * Only marked as processed after successful delivery

---

## 📦 Requirements

These are installed automatically inside Docker:

* **Python 3.13 (slim base image)**
* **Firefox 142.0.1 (Linux 64-bit)**
* **Geckodriver** (you must provide matching binary inside `app/`)
* Python dependencies (`requirements.txt`)
* System libs: `libgtk-3-0`, `libasound2`, `libnss3`, etc.

---

## 📡 Environment & Secrets

* Please read the `env_template.py` to setup and configure all  environment variables or change the project as you need'.
* **Telegram Bot Token** and **Chat ID** should be configured in `env.py` file.

---

## 📑 Example Usage

Run with manual URLs:

```
Enter YouTube video URLs (comma separated), or type 'feed' for RSS feed: https://youtu.be/dQw4w9WgXcQ
```

Run with RSS feed:

```
Enter YouTube video URLs (comma separated), or type 'feed' for RSS feed: feed
```

---
