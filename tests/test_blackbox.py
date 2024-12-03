import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class BlackBoxTesting(StaticLiveServerTestCase):
    def setUp(self):
        """Setup method to run before each test."""
        chrome_options = Options()

        # Check environment variable to determine headless mode
        if os.getenv('ENVIRONMENT') == 'production':  # On Heroku or production environment
            chrome_options.add_argument("--headless")  # Run Chrome in headless mode
            chrome_options.add_argument("--no-sandbox")  # For containerized environments like Heroku
            chrome_options.add_argument("--disable-dev-shm-usage")  # To avoid memory issues
            chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"  # Heroku Chrome binary path
            self.driver = webdriver.Chrome(executable_path=os.environ.get("/app/.chromedriver/bin/chromedriver"), chrome_options=chrome_options)
        
        else:
            # In development, run normally with UI
            chrome_options.add_argument("--start-maximized")  # Open the browser maximized (optional)
            service = Service(ChromeDriverManager().install())  # Use webdriver-manager for local
            # Initialize the Chrome driver with the options
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        
        # Initialize the WebDriver with the ChromeDriverManager to ensure it's always up-to-date
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Wait for elements to load
        self.driver.get("http://127.0.0.1:8000")  # Update with the correct base URL for your app

    def tearDown(self):
        """Teardown method to run after each test."""
        self.driver.quit()

    def test_authentication_empty_password(self):
        """Test submitting the form with an empty password field."""
        self.driver.find_element(By.NAME, "email").send_keys("test@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("")
        self.driver.find_element(By.CLASS_NAME, "login100-form-btn").click()
        self.assertIn("alert-validate", self.driver.page_source)

    def test_authentication_empty_email(self):
        """Test submitting the form with an empty email field."""
        self.driver.find_element(By.NAME, "email").send_keys("")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CLASS_NAME, "login100-form-btn").click()
        self.assertIn("alert-validate", self.driver.page_source)

    def test_authentication_invalid_user(self):
        """Test submitting the form with an email of a user that doesn't exist."""
        self.driver.find_element(By.NAME, "email").send_keys("nonexistent@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CLASS_NAME, "login100-form-btn").click()
        self.assertIn("Email not found.", self.driver.page_source)

    def test_dashboard_click_options(self):
        """Test clicking each of the 5 options on the dashboard."""
        # Login
        self.driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CLASS_NAME, "login100-form-btn").click()

        # Wait for dashboard to load
        time.sleep(4)

        # Get all clickable options (replace the selector with the actual one used in your app)
        options = self.driver.find_elements(By.CLASS_NAME, "topic-heading")

        # Ensure there are 5 options
        self.assertEqual(len(options), 5, "Expected 5 options on the dashboard")

        # Click each option and check it doesn't cause an error
        for index, option in enumerate(options):
            # Scroll to the element to make sure it's clickable
            self.driver.execute_script("arguments[0].scrollIntoView(true);", option)
            time.sleep(0.5)

            # Wait for the element to be visible
            WebDriverWait(self.driver, 10).until(EC.visibility_of(option))
            
            # Click the option
            option.click()
            time.sleep(1)  # Allow page transition/rendering

            # Check that no error occurs
            self.assertNotIn("Error", self.driver.page_source, f"Option {index + 1} caused an error")

            # Go back to the dashboard for the next option
            self.driver.back()
