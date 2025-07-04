# Labubu Pilot 🤖

An intelligent automation tool for monitoring and purchasing Labubu collectibles from Pop Mart's website. The bot automatically scans multiple product URLs, detects availability, and assists with the purchasing process when rare items become available.

## ✨ Features

- 🔍 **Smart Monitoring**: Scans multiple Pop Mart product URLs simultaneously
- 🎯 **Availability Detection**: Automatically detects when products become available
- 🛒 **Purchase Assistance**: Guides users through the purchase process
- 🔔 **Discord Notifications**: Sends alerts to your Discord channel when products are found
- 🔊 **Audio Alerts**: Plays system sound alerts for immediate notification
- 🛡️ **Anti-Detection**: Implements sophisticated measures to avoid bot detection
- ⏱️ **Human-like Behavior**: Simulates natural browsing patterns with random delays
- 📝 **Comprehensive Logging**: Detailed logs of all bot activities
- 🔐 **Secure Login**: Supports environment variables for credential management
- 🌐 **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Google Chrome browser** (latest version recommended)
- **Pop Mart account** with valid credentials
- **Internet connection** with stable bandwidth

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JohnY0920/labubu_pilot.git
   cd labubu_pilot
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (Optional but recommended):
   ```bash
   # Create a .env file in the project directory
   echo "DISCORD_WEBHOOK=your_discord_webhook_url_here" > .env
   echo "POPMART_USERNAME=your_email@example.com" >> .env
   echo "POPMART_PASSWORD=your_password" >> .env
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Discord Integration (Optional)
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your_webhook_url

# Pop Mart Credentials (Optional - will prompt if not provided)
POPMART_USERNAME=your_email@example.com
POPMART_PASSWORD=your_secure_password
```

### Product URLs

The bot is pre-configured to monitor specific Labubu product ranges. To customize the target products, edit the `PRODUCTS` list in `labubu_bot.py`:

```python
# Current configuration monitors products with IDs from 50000-50990
PRODUCTS = [f"https://www.popmart.com/ca/pop-now/set/293-1000{str(i).zfill(4)}00879" for i in range(5000, 5100, 10)]
```

## 🎮 Usage

### Method 1: Direct Python Execution
```bash
python labubu_bot.py
```

### Method 2: Shell Script (macOS/Linux)
```bash
chmod +x run_bot.sh
./run_bot.sh
```

### Bot Workflow

1. **Initialization**: The bot starts up and configures Chrome WebDriver
2. **Authentication**: Logs into Pop Mart using provided credentials
3. **Monitoring**: Continuously scans configured product URLs
4. **Detection**: When a product becomes available, the bot will:
   - ✅ Play an audio alert
   - 📱 Send Discord notification (if configured)
   - 🌐 Keep the browser window open on the product page
   - 📝 Display purchase instructions

5. **Manual Completion**: User completes the purchase manually for security

## 📊 Output & Logging

- **Console Output**: Real-time status updates and progress information
- **Log File**: Detailed logs written to `labubu_pilot.log`
- **Discord Alerts**: Instant notifications when products are found
- **Audio Alerts**: System sound notifications for immediate attention

## 🛡️ Anti-Detection Features

The bot implements several sophisticated measures to maintain stealth:

- **Dynamic User Agents**: Rotates between modern browser identities
- **Human-like Timing**: Random delays between actions (0.5-1.5 seconds)
- **WebDriver Masking**: Removes automation detection signatures
- **Natural Browsing**: Mimics real user interaction patterns
- **Profile Management**: Uses clean browser profiles
- **Error Handling**: Graceful recovery from detection attempts

## 🔧 Advanced Configuration

### Custom Delays
Modify `human_like_delay()` function to adjust timing:
```python
def human_like_delay():
    time.sleep(random.uniform(0.5, 1.5))  # Adjust range as needed
```

### User Agent Rotation
Add custom user agents to the `USER_AGENTS` list for variety.

### Monitoring Frequency
The bot checks products continuously with built-in delays for optimal performance.

## 🚨 Important Notes

- **Manual Purchase**: For security, the bot assists with detection but requires manual purchase completion
- **Rate Limiting**: Built-in delays prevent overwhelming Pop Mart's servers
- **Credential Security**: Use environment variables to protect login information
- **Legal Compliance**: Ensure usage complies with Pop Mart's Terms of Service
- **Browser Updates**: Keep Chrome browser updated for optimal compatibility

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**:
   ```bash
   # Update Chrome to latest version
   # Ensure ChromeDriver is in PATH
   ```

2. **Login Problems**:
   - Verify credentials in `.env` file
   - Check for two-factor authentication requirements
   - Ensure Pop Mart account is active

3. **Detection Issues**:
   - Clear browser cache and cookies
   - Try different user agents
   - Increase delay intervals

### Getting Help

- Check `labubu_pilot.log` for detailed error information
- Ensure all prerequisites are properly installed
- Verify network connectivity and firewall settings

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is provided for educational and personal use only. Users are responsible for:
- Complying with Pop Mart's Terms of Service
- Using the tool ethically and responsibly
- Respecting website rate limits and policies
- Understanding that automated purchasing may violate site terms

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## 📞 Support

For questions and support, please open an issue on the [GitHub repository](https://github.com/JohnY0920/labubu_pilot).

---

**Happy Collecting! 🎁**
