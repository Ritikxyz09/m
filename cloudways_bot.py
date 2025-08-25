from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import os
import time
import asyncio

# ------------------- TELEGRAM BOT TOKEN -------------------
BOT_TOKEN = os.getenv('8105791394:AAG4PPggphTHzoI8HpWZvoy2sl_Qw_DYtVU')

# ------------------- CHROME SETUP FOR GitHub Actions -------------------
def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Headless mode for GitHub
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # GitHub Actions में Chrome setup
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        # Alternative approach
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
    
    return driver

# ------------------- ACCOUNT CREATION FUNCTION -------------------
def create_cloudways_account(email, password):
    driver = None
    try:
        url = f"https://phpstack-1503418-5758174.cloudwaysapps.com/refcw.php?email={email}"
        
        driver = setup_chrome_driver()
        driver.get(url)

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Fill email field
        try:
            email_field = driver.find_element(By.NAME, "email")
            email_field.clear()
            email_field.send_keys(email)
        except:
            print("Email field already filled or not found")
        
        # Fill password field
        try:
            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
        except:
            try:
                password_field = driver.find_element(By.NAME, "pass")
                password_field.send_keys(password)
            except:
                password_field = driver.find_element(By.NAME, "user_password")
                password_field.send_keys(password)
        
        # Submit form
        try:
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
        except:
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
        
        time.sleep(5)
        
        return True, "Account created successfully! Check email for verification."
        
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        if driver:
            driver.quit()

# ------------------- TELEGRAM BOT HANDLERS -------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Cloudways Bot is running on GitHub Actions!")

async def create_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("❌ Format: /create email@example.com password123")
            return
        
        email = context.args[0]
        password = context.args[1]
        
        await update.message.reply_text(f"⏳ Creating account for {email}...")
        
        success, message = await asyncio.to_thread(create_cloudways_account, email, password)
        
        if success:
            await update.message.reply_text(f"✅ {message}")
        else:
            await update.message.reply_text(f"❌ {message}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ------------------- MAIN FUNCTION -------------------
def main():
    if BOT_TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN_HERE':
        print("❌ Please set BOT_TOKEN environment variable")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("create", create_command))
    
    print("🤖 Cloudways Bot Started on GitHub Actions...")
    app.run_polling()

if __name__ == "__main__":
    main()
