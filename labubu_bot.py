from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time
import random
import platform
import requests
import logging
import json
import tempfile
import shutil

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="labubu_bot.log",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

# Discord webhook for notifications
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# List of modern user agents
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
]

# Modify PRODUCTS to iterate through numbers
PRODUCTS = [f"https://www.popmart.com/ca/pop-now/set/293-1000{str(i).zfill(4)}" for i in range(2374, 2400, 10)]

def get_random_user_agent():
    """Get a random user agent from the list of modern browsers."""
    return random.choice(USER_AGENTS)

def human_like_delay():
    """Add a random delay to simulate human behavior."""
    time.sleep(random.uniform(0.5, 1.5))

def play_sound_alert():
    """Play a sound alert when an item is added to cart."""
    try:
        if platform.system() == "Darwin":  # macOS
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        elif platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 1000)
        else:  # Linux
            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
    except Exception as e:
        print(f"⚠️ Could not play sound alert: {str(e)}")

def login(driver, username, password):
    """Log into Pop Mart using provided credentials."""
    print("🔑 Attempting to log in...")
    try:
        driver.get("https://www.popmart.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Log In')]"))).click()
        print("✅ Logged in successfully!")
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")

def get_driver():
    """Setup and return a Chrome webdriver instance with anti-detection measures."""
    print("🔧 Setting up Chrome driver...")
    
    try:
        # Initialize Chrome options
        chrome_options = Options()
        
        # Get the user's Chrome profile directory
        home = os.path.expanduser("~")
        chrome_profile = os.path.join(home, "Library/Application Support/Google/Chrome/Default")
        
        # Create a temporary directory for the profile copy
        temp_dir = tempfile.mkdtemp()
        print(f"📁 Creating temporary profile directory: {temp_dir}")
        
        # Copy the Chrome profile to the temporary directory
        try:
            shutil.copytree(chrome_profile, os.path.join(temp_dir, "Default"))
            print("✅ Successfully copied Chrome profile")
        except Exception as e:
            print(f"⚠️ Could not copy Chrome profile: {str(e)}")
            print("Using fresh profile instead...")
        
        # Configure Chrome options
        chrome_options.add_argument(f"user-data-dir={temp_dir}")
        chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
        
        # Additional options for stability and stealth
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Performance optimizations
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Disable images for faster loading
        chrome_options.add_argument("--disable-javascript")  # Disable JavaScript for faster loading
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disk-cache-size=1")  # Minimize disk cache
        chrome_options.add_argument("--media-cache-size=1")  # Minimize media cache
        chrome_options.add_argument("--disable-application-cache")  # Disable app cache
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Create the driver
        print("🚀 Creating Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Execute CDP commands to prevent detection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        
        print("✅ Chrome driver created successfully")
        driver.set_page_load_timeout(10)  
        driver.implicitly_wait(3) 
        
        return driver
        
    except Exception as e:
        print(f"❌ Failed to create Chrome driver: {str(e)}")
        raise

def add_to_cart(driver, url):
    """Attempt to add a product to the cart using the new process."""
    print("🔄 Starting add_to_cart process...")
    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Click "Buy Multiple Boxes"
        buy_multiple_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ant-btn-ghost.index_chooseMulitityBtn__n0MoA"))
        )
        buy_multiple_btn.click()
        print("✅ Clicked 'Buy Multiple Boxes'")
        
        # Wait and click "Select all"
        time.sleep(1)
        select_all_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Select all')]"))
        )
        select_all_btn.click()
        print("✅ Clicked 'Select all'")
        
        # Click "ADD TO BAG"
        add_to_bag_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ant-btn-primary.index_btn__Y5dKo"))
        )
        add_to_bag_btn.click()
        print("✅ Clicked 'ADD TO BAG'")
        
        return True
    except Exception as e:
        print(f"❌ Error in add_to_cart: {str(e)}")
        return False

def check_product_availability(driver, url):
    """Check if a product is available without adding to cart."""
    try:
        print(f"🔍 Checking availability for: {url}")
        driver.get(url)
        
        # Wait for the page to load with reduced timeout
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Look for the add to bag button
        try:
            add_btn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.index_usBtn__2KlEx.index_red__kx6Ql.index_btnFull__F7k90"))
            )
            print(f"✅ Product is available: {url}")
            return True
        except:
            try:
                add_btn = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'ADD TO BAG')]"))
                )
                print(f"✅ Product is available: {url}")
                return True
            except:
                print(f"❌ Product is not available: {url}")
                return False
    except Exception as e:
        print(f"❌ Error checking availability: {str(e)}")
        return False

def run_bot_cycle():
    """Run one cycle of the bot, checking all products for availability."""
    driver = None
    try:
        print("\n🌐 Starting product checks...")
        
        try:
            driver = get_driver()
            print("✅ Created main browser window")
            login(driver, "your_username", "your_password")  # Add login step
        except Exception as e:
            print(f"❌ Failed to create driver or log in: {str(e)}")
            return
        
        for product_url in PRODUCTS:
            print(f"\n🔍 Checking product: {product_url}")
            result = add_to_cart(driver, product_url)
            if result:
                print(f"✅ Successfully added to cart: {product_url}")
                break  # Stop after first successful addition
            else:
                print(f"❌ Failed to add to cart: {product_url}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        if driver:
            driver.quit()
        print("✨ Bot session ended")

def run_bot():
    """Main function to run the bot continuously."""
    print("\n🤖 Starting bot...")
    print("🎯 Target products:")
    for i, product in enumerate(PRODUCTS, 1):
        print(f"{i}. {product}")
    print("⏰ TEST MODE: Running immediately")
    
    while True:
        run_bot_cycle()

if __name__ == "__main__":
    print("\n🚀 Starting Labubu Bot...")
    print("=" * 50)
    print("⚠️ IMPORTANT: Make sure you're logged into Pop Mart in your regular Chrome!")
    print("⏰ TEST MODE: Running immediately")
    print("=" * 50)
    
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot stopped due to error: {str(e)}")
    finally:
        print("\n✨ Bot session ended")