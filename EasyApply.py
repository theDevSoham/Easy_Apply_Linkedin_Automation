from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from LinkedinLinks import LinkedinLinks
import time

class EasyApply:

	def __init__(self, data):
		self.email = data["email"]
		self.password = data["password"]
		self.filters = data["filters"] or []
		self.driver = self.__setup_driver()

	def __setup_driver(self):
		# Configure options for ChromeDriver
		options = Options()
		options.add_argument("--start-maximized")  # Start browser maximized
		options.add_argument("--disable-infobars")
		options.add_argument("--disable-extensions")

		# Initialize the ChromeDriver
		service = Service(ChromeDriverManager().install())
		driver = webdriver.Chrome(service=service, options=options)
		return driver

	def login(self):

		# Open LinkedIn login page
		self.driver.get(LinkedinLinks.get_url(LinkedinLinks.LOGIN))

		# Enter username
		username_input = self.driver.find_element(By.ID, "username")
		username_input.send_keys(self.email)  # Replace with your LinkedIn username

		# Enter password
		password_input = self.driver.find_element(By.ID, "password")
		password_input.send_keys(self.password)  # Replace with your LinkedIn password

		# Submit the login form
		password_input.send_keys(Keys.RETURN)
		
		# Wait for login to finish
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "global-nav-search")))

	def search_jobs(self, keyword_info: dict = {"title": "", "location": ""}):
		self.driver.get(LinkedinLinks.get_url(LinkedinLinks.SEARCH_JOB))

		# title of job input
		title_input = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-keyword')]")
		title_input.clear()
		title_input.send_keys(keyword_info["title"])

		# location of job input
		location_input = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-location')]")
		location_input.clear()
		location_input.send_keys(keyword_info["location"])

		# Submit the login form
		title_input.send_keys(Keys.RETURN)

		# Wait for job search to finish
		WebDriverWait(self.driver, 20, 5).until(EC.presence_of_element_located((By.XPATH, "//button[text()='All filters']")))

	def easy_apply_filter(self):
		all_filters = self.driver.find_element(By.XPATH, "//button[text()='All filters']")
		all_filters.click()

		time.sleep(2)

		easy_apply_button = self.driver.find_element(By.XPATH, "//h3[text()='Easy Apply']/following-sibling::div//input[@type='checkbox']")
		time.sleep(1)
		
		# Scroll into view if needed and click to toggle the switch
		actions = ActionChains(self.driver)
		actions.move_to_element(easy_apply_button).click().perform()

		# apply filter
		show_results_button = self.driver.find_element(By.XPATH, "//button[@data-test-reusables-filters-modal-show-results-button='true']")
		show_results_button.click()

		time.sleep(3)
