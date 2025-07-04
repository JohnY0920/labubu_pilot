# Labubu Bot 🤖

An automated bot for monitoring and purchasing Labubu products from Pop Mart's website. The bot automatically checks product availability and attempts to add items to cart when they become available.

## Features

- 🔍 Monitors multiple Pop Mart products simultaneously
- 🛒 Automatically adds products to cart when available
- 🔔 Sends Discord notifications for successful cart additions
- 🔊 Plays sound alerts on successful cart additions
- 🛡️ Implements anti-bot detection measures
- ⏱️ Human-like behavior simulation
- 📝 Detailed logging of all activities

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Pop Mart account (must be logged in to Chrome)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/andryuxiong/labububot.git
cd labubu-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory:
```
DISCORD_WEBHOOK=your_discord_webhook_url_here
```

## Configuration

1. Add your target products to the `PRODUCTS` list in `labubu_bot.py`:
```python
PRODUCTS = [
    "https://www.popmart.com/us/products/YOUR-PRODUCT-ID/PRODUCT-NAME",
    # Add more products here
]
```

2. Make sure you're logged into Pop Mart in your regular Chrome browser before running the bot.

## Usage

Run the bot:
```bash
python labubu_bot.py
```

The bot will:
1. Start monitoring the specified products
2. Check availability every few seconds
3. Attempt to add products to cart when available
4. Send Discord notifications and play sound alerts on success

## Output

- Logs are written to `labubu_bot.log`
- Discord notifications are sent for successful cart additions
- Sound alerts play on successful cart additions

## Anti-Detection Measures

The bot implements several measures to avoid detection:
- Random delays between actions
- Human-like behavior simulation
- Chrome profile copying
- WebDriver detection prevention
- Multiple click methods
- Random user agent rotation

## Notes

- The bot uses your Chrome profile to maintain login state
- Make sure to keep your Chrome browser updated
- The script can be stopped at any time with Ctrl+C
- Discord notifications require a valid webhook URL

## Disclaimer

This tool is for educational purposes only.
