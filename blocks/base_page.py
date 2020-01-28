import logging
import time

import allure
import pytest
from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ex_cond
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(filename="logs.log", level=logging.INFO)


class BasePage:


    def __init__(self, driver):
        self._driver = driver
        driver.implicitly_wait(3)
        logging.info(">>>>>>>>>>>>>>> INITIALIZATION NEW DRIVER <<<<<<<<<<<<<<<")
        self.navigate_to('https://doc-stg.telemed.care/cabinet')

    def navigate_to(self, url):
        logging.info("Open url: " + str(url))
        self._driver.get(url)


    def get_element(self, locator, timeout=5):
        logging.info("Get element " + str(locator)) 
        return WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_element_located(locator), ' : '.join(locator))
        
        
    def get_elements(self, locator, timeout=5):
        logging.info("Get elements " + str(locator)) 
        return WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_any_elements_located(locator), ' : '.join(locator))


    def send_keys(self, locator, timeout=5, value=None):
        logging.info("Send keys \"" + str(value) + "\" to " + str(locator)) 
        WebDriverWait(self._driver, timeout).until(
            ex_cond.element_to_be_clickable(locator), ' : '.join(locator)).send_keys(value)
        
        
    def get_url(self):
        logging.info("Get current url") 
        return self._driver.current_url


    def refresh(self):
        logging.info("Refresh page")
        self._driver.refresh()


    def click(self, locator, timeout=5):
        logging.info("Click to element " + str(locator))
        WebDriverWait(self._driver, timeout).until(
        ex_cond.element_to_be_clickable(locator), ' : '.join(locator)).click()


    def get_shadow_element(self, parent, locator):
        root = self._driver.find_element_by_tag_name(parent)
        shadow_root = self._driver.execute_script('return arguments[0].shadowRoot', root) 
        return shadow_root.find_element_by_css_selector(locator)


    def page_source(self):
        return self._driver.page_source
        

    def is_exist(self, locator):
        
        try:
            self.get_element(locator, timeout=1)
        except TimeoutException:
            logging.info("Checking is exist element " + str(locator) + " (Not visible)")
            return False
        else:
            logging.info("Checking is exist element " + str(locator) + " (Visible)")
            return True
