# TeleData — Telegram Channel Downloader

A desktop GUI app for downloading all messages and media from Telegram channels.  
Built with Python + CustomTkinter + Telethon.

## Features

- Download all messages from any public/private Telegram channel
- Organizes media into `photos/`, `videos/`, `other/` folders
- Saves message data to `messages.xlsx`
- Resume support — continues from last downloaded message
- Date range filtering
- MTProto & HTTP proxy support
- Persian (RTL) / English UI
- Light/Dark theme
- Concurrent downloads (1–10 simultaneous)

## Setup

### 1. Get Telegram API credentials

Go to [my.telegram.org](https://my.telegram.org) → API Development Tools → create an app.  
You'll get an **API ID** and **API Hash**.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
python TeleData.py
```

## First Use

1. Open **Settings → API Settings** and enter your API ID & API Hash
2. Go to **Settings → Authentication** → enter your phone number → verify with the SMS code
3. Go to **Settings → Channel Settings** → enter the channel username (without `@`)
4. Click **Run** from the main menu

Your credentials are saved locally in `config.json` (excluded from git).

## File Structure

```
TeleData.py          # Main application
requirements.txt     # Python dependencies
config.json          # Your settings (auto-created, gitignored)
session*             # Telegram session (auto-created, gitignored)
messages.xlsx        # Downloaded message data (gitignored)
media/
  photos/
  videos/
  other/
```

## Developer

[@immdjavad](https://t.me/immdjavad)
