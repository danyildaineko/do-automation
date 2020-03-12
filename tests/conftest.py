#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver

from blocks.main import MainPage


@pytest.yield_fixture(scope = "session")
def driver():
    browser = webdriver.Chrome(executable_path = '/Users/eckoda/Documents/chromedriver')
    # browser.get('URL HERE')
    login_page = MainPage(browser)
    login_page.login('NUMBER HERE', u'укр')
    yield browser

    browser.close()
