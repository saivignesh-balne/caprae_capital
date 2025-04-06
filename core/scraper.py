from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import config

class LinkedInScraper:
    def __init__(self, headless=False):
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless=new")
        
        # Anti-detection settings
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.set_page_load_timeout(30)
        self._logged_in = False  # Internal login state tracker

    def is_logged_in(self):
        """Check if the scraper is logged in to LinkedIn"""
        return self._logged_in

    def login(self, automatic=True):
        """Handle LinkedIn login with optional automatic or manual mode"""
        self.driver.get(config.CONFIG['linkedin']['login_url'])
        time.sleep(random.uniform(1, 3))
        
        if automatic:
            # Enter credentials automatically
            email_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, 'username')))
            email_field.send_keys(config.CONFIG['linkedin']['email'])
            
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(config.CONFIG['linkedin']['password'])
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Wait for login completion or verification
        try:
            WebDriverWait(self.driver, 20).until(
                lambda d: "linkedin.com/feed" in d.current_url or
                        "linkedin.com/home" in d.current_url or
                        "checkpoint/challenge" in d.current_url)
            
            if "checkpoint/challenge" in self.driver.current_url:
                print("\n=== MANUAL VERIFICATION REQUIRED ===")
                print("1. Complete verification in the browser window")
                print("2. Wait until you see LinkedIn home page")
                print("3. Return to the web interface")
                print("4. Click the 'Scrape' button")
                print("="*40)
                
                # Wait for user to complete verification
                while "checkpoint/challenge" in self.driver.current_url:
                    time.sleep(1)
            
            self._logged_in = True
            return True
            
        except Exception as e:
            self._logged_in = False
            raise Exception(f"Login failed: {str(e)}")

    def scrape_profile(self, profile_url):
        """Scrape a LinkedIn profile"""
        if not self._logged_in:
            raise Exception("Not logged in - please login first")
        
        try:
            self.driver.get(profile_url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            name = soup.find('h1').get_text().strip() if soup.find('h1') else None
            headline = soup.find('div', {'class': 'text-body-medium'})
            
            return {
                'name': name,
                'headline': headline.get_text().strip() if headline else None,
                'profile_url': profile_url,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            raise Exception(f"Scraping failed: {str(e)}")

    def close(self):
        """Clean up the scraper"""
        if hasattr(self, 'driver'):
            self.driver.quit()
        self._logged_in = False