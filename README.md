# Labubu Pilot 🤖

> **Note**: This project is a fork and enhanced version of the original [labububot](https://github.com/andryuxiong/labububot) by [@andryuxiong](https://github.com/andryuxiong). Thanks to the original author for the foundation!

An automated monitoring tool for checking Labubu product availability on Pop Mart's website. The bot scans multiple product URLs in one cycle, detects available products, and keeps the browser open for manual purchase completion.

## ✨ Features

- 🔍 **Smart Monitoring**: Scans multiple Pop Mart product URLs in one cycle
- 🎯 **Availability Detection**: Automatically detects when products become available
- 🛒 **Manual Purchase Support**: Keeps browser open on available product page
- 🔊 **Audio Alerts**: Plays system sound alerts when products are found
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
   echo "POPMART_USERNAME=your_email@example.com" > .env
   echo "POPMART_PASSWORD=your_password" >> .env
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
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
3. **Single Scan**: Checks each configured product URL once for availability
4. **Detection**: When a product becomes available, the bot will:
   - ✅ Play an audio alert
   - 🌐 Keep the browser window open on the product page
   - 📝 Display purchase instructions
   - ⏳ Wait for user to manually complete purchase

5. **Manual Purchase**: User completes the purchase manually in the open browser

> **Note**: The bot runs ONE cycle and stops. To continuously monitor, you need to run it multiple times or modify the code for continuous checking.

## 📊 Output & Logging

- **Console Output**: Real-time status updates and progress information
- **Log File**: Detailed logs written to `labubu_pilot.log`
- **Audio Alerts**: System sound notifications when products are found
- **Browser Window**: Stays open on available product page for manual purchase

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

### Continuous Monitoring
To make the bot continuously check products, you can:

1. **Use a loop script**:
   ```bash
   while true; do
     python labubu_bot.py
     sleep 30  # Wait 30 seconds between cycles
   done
   ```

2. **Modify the code** to add a loop in the `run_bot()` function

## 🚨 Important Notes

- **Single Cycle**: Bot checks products once and stops (not continuous)
- **Manual Purchase**: Bot assists with detection but requires manual purchase completion
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

## 🙏 Acknowledgments

- **Original Project**: This is a fork of [labububot](https://github.com/andryuxiong/labububot) by [@andryuxiong](https://github.com/andryuxiong)

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
