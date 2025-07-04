"""
Labubu Pilot - An intelligent automation tool for monitoring Labubu collectibles
GitHub: https://github.com/JohnY0920/labubu_pilot
License: MIT
"""

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
    filename="labubu_pilot.log",
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

# Target URLs with larger number range: 293-1000{iteration_number}00879, increments of 10
PRODUCTS = [f"https://www.popmart.com/ca/pop-now/set/293-1000{str(i).zfill(4)}00879" for i in range(5000, 5100, 10)]

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
    """Log into Pop Mart using provided credentials with the correct login flow."""
    print("🔑 Attempting to log in...")
    try:
        # Navigate to the login page
        print("📱 Navigating to login page...")
        driver.get("https://www.popmart.com/ca/user/login")
        print(f"🌐 Current URL: {driver.current_url}")
        human_like_delay()
        
        # Dismiss any overlays first
        dismiss_overlays(driver)
        
        # Wait for and click the email input field
        print("📧 Looking for email input field...")
        email_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "email"))
        )
        email_input.clear()
        email_input.send_keys(username)
        print("✅ Entered email address")
        human_like_delay()
        
        # Click the CONTINUE button
        print("🔄 Looking for CONTINUE button...")
        continue_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ant-btn.ant-btn-primary.index_loginButton__O6r8l"))
        )
        safe_click(driver, continue_btn)
        print("✅ Clicked CONTINUE button")
        
        # Wait a bit longer for page transition
        time.sleep(3)
        print(f"🌐 Current URL after continue: {driver.current_url}")
        
        # Wait for password page and enter password
        print("🔒 Looking for password input field...")
        password_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password_input.clear()
        password_input.send_keys(password)
        print("✅ Entered password")
        human_like_delay()
        
        # Click the SIGN IN button
        print("🔐 Looking for SIGN IN button...")
        signin_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ant-btn.ant-btn-primary.index_loginButton__O6r8l"))
        )
        safe_click(driver, signin_btn)
        print("✅ Clicked SIGN IN button")
        
        # Wait for login to complete (check for redirect or success indicator)
        print("⏳ Waiting for login to complete...")
        time.sleep(5)  # Give it time to process
        
        # Check if we're still on login page or redirected
        current_url = driver.current_url
        print(f"🌐 Final URL: {current_url}")
        
        if "login" not in current_url.lower():
            print("✅ Logged in successfully!")
        else:
            print("⚠️ Still on login page, but continuing...")
        
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        print(f"🌐 Current URL when error occurred: {driver.current_url}")
        # Don't raise the exception, just continue - login might have worked
        print("🔄 Continuing with the process...")

def get_driver():
    """Setup and return a Chrome webdriver instance with anti-detection measures."""
    print("🔧 Setting up Chrome driver...")
    
    try:
        # Initialize Chrome options
        chrome_options = Options()
        
        # Configure Chrome options for better compatibility
        chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
        
        # Essential options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Remove performance options that might cause issues
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins-discovery")
        
        # Remove JavaScript and image disabling - we need these for login
        # chrome_options.add_argument("--disable-javascript")  # REMOVED - needed for login
        # chrome_options.add_argument("--disable-images")  # REMOVED - might be needed
        
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
        driver.set_page_load_timeout(30)  # Increased timeout
        driver.implicitly_wait(5)  # Increased implicit wait
        
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
        
        # Dismiss any overlays that might interfere
        dismiss_overlays(driver)
        time.sleep(1)
        
        # Click "Buy Multiple Boxes"
        buy_multiple_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ant-btn-ghost.index_chooseMulitityBtn__n0MoA"))
        )
        safe_click(driver, buy_multiple_btn)
        print("✅ Clicked 'Buy Multiple Boxes'")
        
        # Wait and click "Select all"
        time.sleep(1)
        select_all_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Select all')]"))
        )
        safe_click(driver, select_all_btn)
        print("✅ Clicked 'Select all'")
        
        # Click "ADD TO BAG"
        add_to_bag_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ant-btn-primary.index_btn__Y5dKo"))
        )
        safe_click(driver, add_to_bag_btn)
        print("✅ Clicked 'ADD TO BAG'")
        
        return True
    except Exception as e:
        print(f"❌ Error in add_to_cart: {str(e)}")
        return False

def check_product_availability(driver, url):
    """Check if a product is available and return True if found."""
    try:
        print(f"🔍 Checking availability for: {url}")
        driver.get(url)
        
        # Wait for the page to load with reduced timeout
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Dismiss any overlays that might interfere
        dismiss_overlays(driver)
        time.sleep(1)
        
        # Look for the "Buy Multiple Boxes" button which indicates product is available
        try:
            buy_multiple_btn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.ant-btn-ghost.index_chooseMulitityBtn__n0MoA"))
            )
            if buy_multiple_btn.is_displayed():
                print(f"🎯 PRODUCT FOUND! Available at: {url}")
                return True
        except:
            pass
            
        # Alternative check for add to bag button
        try:
            add_btn = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.index_usBtn__2KlEx.index_red__kx6Ql.index_btnFull__F7k90"))
            )
            if add_btn.is_displayed():
                print(f"🎯 PRODUCT FOUND! Available at: {url}")
                return True
        except:
            pass
            
        # Another alternative check
        try:
            add_btn = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'ADD TO BAG')]"))
            )
            if add_btn.is_displayed():
                print(f"🎯 PRODUCT FOUND! Available at: {url}")
                return True
        except:
            pass
            
        print(f"❌ Product not available: {url}")
        return False
        
    except Exception as e:
        print(f"❌ Error checking availability: {str(e)}")
        return False

def dismiss_overlays(driver):
    """Dismiss any overlays, popups, or policy notices that might intercept clicks."""
    try:
        # Try to dismiss policy overlay
        policy_overlay = driver.find_element(By.CSS_SELECTOR, "div.policy_aboveFixedContainer__KfeZi")
        if policy_overlay.is_displayed():
            print("🚫 Found policy overlay, attempting to dismiss...")
            # Try to find and click close button
            close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='close'], button[class*='dismiss'], .close, .dismiss")
            for btn in close_buttons:
                try:
                    if btn.is_displayed():
                        btn.click()
                        print("✅ Dismissed overlay")
                        time.sleep(1)
                        return True
                except:
                    continue
            
            # Try clicking outside the overlay
            try:
                driver.execute_script("arguments[0].style.display = 'none';", policy_overlay)
                print("✅ Hidden overlay with JavaScript")
                return True
            except:
                pass
                
    except Exception as e:
        print(f"⚠️ No overlay found or error dismissing: {str(e)}")
    
    return False

def safe_click(driver, element):
    """Safely click an element, handling overlays and using JavaScript if needed."""
    try:
        # First try normal click
        element.click()
        return True
    except Exception as e:
        if "element click intercepted" in str(e):
            print("⚠️ Click intercepted, trying to dismiss overlays...")
            dismiss_overlays(driver)
            time.sleep(1)
            
            # Try clicking again
            try:
                element.click()
                return True
            except:
                # Use JavaScript click as fallback
                print("🔧 Using JavaScript click as fallback...")
                driver.execute_script("arguments[0].click();", element)
                return True
        else:
            raise e

def run_bot_cycle():
    """Run one cycle of the bot, checking all products for availability."""
    driver = None
    product_found = False
    try:
        print("\n🌐 Starting product checks...")
        
        # Create fresh driver for each cycle
        driver = get_driver()
        print("✅ Created main browser window")
        
        # Get login credentials from environment or user input
        username = os.getenv("POPMART_USERNAME")
        password = os.getenv("POPMART_PASSWORD")
        
        if not username or not password:
            print("⚠️ No login credentials found in environment variables.")
            print("💡 You can either:")
            print("   1. Set POPMART_USERNAME and POPMART_PASSWORD environment variables")
            print("   2. Enter credentials manually below")
            print()
            
            if not username:
                username = input("Enter your Pop Mart email: ").strip()
            if not password:
                import getpass
                password = getpass.getpass("Enter your Pop Mart password: ").strip()
        
        # Login with provided credentials
        login(driver, username, password)
        
        # Process each product - just check availability, don't add to cart
        for product_url in PRODUCTS:
            print(f"\n🔍 Checking product: {product_url}")
            if check_product_availability(driver, product_url):
                print(f"🎯 PRODUCT FOUND AND AVAILABLE!")
                print(f"🌐 URL: {product_url}")
                play_sound_alert()
                product_found = True
                print("\n🛒 Product is available! Browser window will remain open for you to complete the purchase manually.")
                print("📝 To complete your purchase:")
                print("   1. The product page is already loaded")
                print("   2. Click 'Buy Multiple Boxes' or 'ADD TO BAG'")
                print("   3. Complete the purchase process")
                print("   4. Close the browser when done")
                print("\n⏳ Browser window will stay open. Press Ctrl+C to close the bot when you're finished.")
                break  # Stop after first available product found
            else:
                print(f"❌ Product not available: {product_url}")
        
    except Exception as e:
        print(f"\n❌ Error in bot cycle: {str(e)}")
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    finally:
        if not product_found and driver:
            # Only close driver if no product was found
            try:
                driver.quit()
                print("✅ Driver closed properly")
            except Exception as e:
                print(f"⚠️ Error closing driver: {str(e)}")
        elif product_found and driver:
            print("🔄 Browser window kept open - product page loaded and ready for manual purchase")
            # Keep the driver open - don't quit it
            try:
                # Wait indefinitely until user interrupts
                while True:
                    time.sleep(60)  # Sleep for 1 minute intervals
            except KeyboardInterrupt:
                print("\n👋 Closing browser as requested by user")
                try:
                    driver.quit()
                    print("✅ Driver closed properly")
                except Exception as e:
                    print(f"⚠️ Error closing driver: {str(e)}")
        
        if not product_found:
            print("✨ Bot session ended - no available products found")
        else:
            print("✨ Bot session ended - browser closed")

def run_bot():
    """Main function to run the bot - production configuration."""
    print("\n🤖 Starting bot...")
    print("🎯 Target products (Production URLs):")
    for i, product in enumerate(PRODUCTS, 1):
        print(f"{i:2d}. {product}")
    print(f"\n📊 Total URLs to check: {len(PRODUCTS)}")
    print("🔄 Production mode: Checking target URLs")
    
    # Run single cycle for production
    run_bot_cycle()

if __name__ == "__main__":
    print("\n🚀 Starting Labubu Pilot...")
    print("=" * 50)
    print("🔐 LOGIN: Bot will ask for credentials or use environment variables")
    print("💡 To set environment variables:")
    print("   export POPMART_USERNAME='your_email@example.com'")
    print("   export POPMART_PASSWORD='your_password'")
    print("🔄 Production mode: Checking target URLs")
    print("=" * 50)
    
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot stopped due to error: {str(e)}")
    finally:
        print("\n✨ Bot session ended")