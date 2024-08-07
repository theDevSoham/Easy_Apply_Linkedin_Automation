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

		time.sleep(2) # TODO: To be replaced with WebDriverWait

		easy_apply_button = self.driver.find_element(By.XPATH, "//h3[text()='Easy Apply']/following-sibling::div//input[@type='checkbox']")
		time.sleep(1) # TODO: To be replaced with WebDriverWait
		
		# Scroll into view if needed and click to toggle the switch
		actions = ActionChains(self.driver)
		actions.move_to_element(easy_apply_button).click().perform()

		time.sleep(3) # TODO: To be replaced with WebDriverWait

	def other_filters(self):
		actions = ActionChains(self.driver)
		
		for filter in self.filters:

			# Remote filters
			if filter == "On-site":
				remote_filter = self.driver.find_element(By.ID, "advanced-filter-workplaceType-1")
				actions.move_to_element(remote_filter).click().perform()

			if filter == "Remote":
				remote_filter = self.driver.find_element(By.ID, "advanced-filter-workplaceType-2")
				actions.move_to_element(remote_filter).click().perform()


			if filter == "Hybrid":
				hybrid_filter = self.driver.find_element(By.ID, "advanced-filter-workplaceType-3")
				actions.move_to_element(hybrid_filter)
			
			time.sleep(2) # TODO: To be replaced with WebDriverWait

	# apply filters
	def apply_all_filters(self):
		show_results_button = self.driver.find_element(By.XPATH, "//button[@data-test-reusables-filters-modal-show-results-button='true']")
		show_results_button.click()

	def find_offers(self):
		total_number_of_offers = self.driver.find_element(By.CSS_SELECTOR, "div.jobs-search-results-list__subtitle").text.split(" ")[0].replace(",", "")
		print(f"total number of offers found: {int(total_number_of_offers)}")

		results_list = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'jobs-search-results__list-item')]")
		print(f"All jobs list in current page: {results_list}")

		for result in results_list:
			hover = ActionChains(self.driver).move_to_element(result)
			hover.click().perform()
			time.sleep(2)
