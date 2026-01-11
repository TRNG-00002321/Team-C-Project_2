"""
cross_browser_automated.py
Automated driver setup for all major browsers
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def create_driver(browser_name: str, headless: bool = False):
    selenium_url = os.getenv('SELENIUM_URL')

    if browser_name == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")

        options.add_experimental_option(
            "prefs",
            {
                "profile.password_manager_leak_detection": False,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            }
        )
    
    elif browser_name == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")

    if selenium_url:
        max_retries = 30
        retry_delay = 1
        
        for _ in range(max_retries):
            try:
                driver = webdriver.Remote(
                    command_executor=selenium_url,
                    options=options
                )
                print("Successfully connected to Selenium Grid")
                return driver
            except Exception as e:
                print(f"Connection failed: {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
        else:
            raise RuntimeError(f'Could not connect to Selenium Grid at {selenium_url} after {max_retries} attempts')

    print(f"Selenium Grid unavailable, using local {browser_name} driver")
    return create_driver_old(browser_name, headless)

def create_driver_old(browser_name: str, headless: bool = False):
    browser = browser_name.lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")

        options.add_experimental_option(
            "prefs",
            {
                "profile.password_manager_leak_detection": False,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            }
        )

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")

        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
