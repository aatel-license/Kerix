# Κέριξ (Kérix)
![Alt text](https://github.com/aatel-license/kerix/blob/main/kerix.png "kerix")

*A hybrid news pipeline that extracts article content from RSS feeds and direct URLs, then sends the processed text to a callback endpoint.*


> Κέριξ (Kérix) "Messaggero" — chi consegna i messaggi via webhook. Il nome riflette l'essenza del progetto: estrarre e preservare i contenuti significativi dalle pagine web.

## Overview

This project provides two implementations:

- **Node.js** (`app.js`) — Lightweight article extraction using Mozilla's Readability
- **Python** (`app.py`) — Full-featured hybrid pipeline with RSS feed parsing and batch/stream processing

---

## Node.js Implementation

### Features

- Extracts readable content from web pages using [Mozilla Readability](https://github.com/mozilla/readability)
- Clean text output stripped of navigation, ads, and scripts
- Simple REST API endpoint

### Prerequisites

- Node.js (v14 or higher)
- npm

### Installation

```bash
npm install
```

### Running the Server

```bash
npm start
```

The server starts on `http://localhost:3001`.

### API Endpoint

#### POST `/extract`

Extracts the main article content from a given URL.

**Request Body:**

```json
{
  "url": "https://example.com/article"
}
```

**Response (Success):**

```json
{
  "title": "Article Title",
  "text": "Cleaned text content of the article..."
}
```

**Response (Error):**

```json
{
  "error": "No content extracted"
}
```

---

## Python Implementation

### Features

- Hybrid input: RSS feeds + direct URLs
- Async processing for performance
- Two modes: batch and streaming
- Automatic callback to a user-specified webhook URL
- Content cleaning (removes scripts, styles, junk patterns)
- Built with FastAPI, Scrapling, httpx

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
pip install fastapi pydantic feedparser scrapling httpx uvicorn
```

### Running the Server

```bash
python app.py
```

The server starts on `http://0.0.0.0:8070`.

For development with auto-reload, ensure `uvicorn` is installed and run:

```bash
uvicorn app:app --host 0.0.0.0 --port 8070 --reload
```

### API Endpoints

#### POST `/hybrid_batch`

Processes all URLs in batch mode, then sends callbacks for each extracted article.

**Request Body:**

```json
{
  "rss_feeds": ["https://example.com/rss", "https://blog.example.com/feed"],
  "urls": ["https://example.com/some-article"],
  "callback_url": "https://your-server.com/webhook"
}
```

**Response:**

```json
{
  "status": "completed",
  "processed": 12,
  "total_urls": 15
}
```

#### POST `/stream`

Processes URLs one by one and sends callbacks immediately after each extraction. Useful for large datasets to avoid memory issues.

**Request Body:** (same as `/hybrid_batch`)

```json
{
  "rss_feeds": ["https://example.com/rss"],
  "urls": [],
  "callback_url": "https://your-server.com/webhook"
}
```

### Request Parameters

| Parameter       | Type     | Required | Description                              |
|-----------------|----------|----------|------------------------------------------|
| `rss_feeds`    | Array    | No       | List of RSS/Atom feed URLs               |
| `urls`         | Array    | No       | List of direct article URLs              |
| `callback_url` | String   | Yes      | Webhook URL to receive extracted content |

### How It Works

1. **URL Collection**: Fetches article links from RSS feeds and combines with provided URLs
2. **Content Extraction**: Scrapes each URL, cleans the HTML, and extracts readable text
3. **Callback**: Sends cleaned text to your `callback_url` via POST request

---

## Dependencies

### Node.js

| Package                  | Version  | Purpose                         |
|--------------------------|----------|---------------------------------|
| `express`                | ^5.2.1   | Web framework                   |
| `axios`                  | ^1.15.0  | HTTP client                     |
| `jsdom`                  | ^29.0.2  | HTML parsing                    |
| `@mozilla/readability`   | ^0.6.0   | Article content extraction      |

### Python

| Package       | Purpose                           |
|---------------|-----------------------------------|
| fastapi       | Web framework                     |
| pydantic      | Request validation                |
| feedparser    | RSS/Atom feed parsing             |
| scrapling     | Web scraping                      |
| httpx         | Async HTTP client                 |
| uvicorn       | ASGI server                       |

---

## License

ISC
