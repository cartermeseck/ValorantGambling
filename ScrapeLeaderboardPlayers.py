from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

#Not used currently, but could be useful later, possibly in click_loadmore_button
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Intialize webdriver (webpage)
driver = webdriver.Chrome()






driver.get("https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=global")

#driver.get('https://tracker.gg/valorant/profile/riot/' + name + '/overview')

driver.close()
