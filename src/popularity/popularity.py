import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Popularity:

    def __init__(self, day, time):
        self.day = day
        self.time = time
        self.place_url = os.environ.get('PLACE_URL')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager(
            log_level=0).install(), options=self._web_driver_options)

    def get_popularity(self):
        percentage = None
        self.driver.get(self.place_url)
        try:
            percentage = self.parse_request()
        except Exception as e:
            print(e)
            raise Exception("Error parsing request")
        if (percentage is None):
            raise Exception("Percentage invalid")
        return percentage

    def parse_request(self):
        days_elements = self.driver.find_elements(By.CSS_SELECTOR, '.g2BVhd')
        selected_day_element = self._days_elements_valid(days_elements)
        hours_elements = selected_day_element.find_elements(
            By.CSS_SELECTOR, '.dpoVLd')
        selected_hour_element = self._hours_elements_valid(hours_elements)[
            self.time - 6]
        percentage = self._hour_element_valid(selected_hour_element)
        return percentage

    @property
    def _web_driver_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--lang=pt-BR')
        return options

    def _days_elements_valid(self, days_elements):
        if (len(days_elements) < 7):
            raise Exception("Days elements invalid")
        return days_elements[self.day]

    def _hours_elements_valid(self, current_day_element):
        if (len(current_day_element) < 18):
            raise Exception("Current day element invalid")
        return current_day_element

    def _hour_element_valid(self, current_hour_element):
        aria_label = current_hour_element.get_attribute('aria-label')
        if (aria_label is None):
            raise Exception("Current hour element invalid")
        if (len(aria_label.split(' ')) < 4):
            raise Exception("Current hour element invalid")
        final_percentage = int(aria_label.split(' ')[3].replace('%.', ''))
        if (final_percentage is None or final_percentage < 0 or final_percentage > 100):
            raise Exception("Current hour element invalid")
        return final_percentage
