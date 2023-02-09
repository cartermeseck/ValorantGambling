from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome()
driver.get('https://tracker.gg/valorant/profile/riot/funbunsz%23TTV/overview')

time.sleep(2)

driver.close()