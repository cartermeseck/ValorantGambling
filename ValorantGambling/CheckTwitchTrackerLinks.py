from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

TwitchTrackerLinks = pd.read_csv('TwitchUsernameTrackerLink.csv')
TwitchTrackerLinks['Error'] = "None"


#Intialize webdriver (webpage)
driver = webdriver.Chrome()


for index, row in TwitchTrackerLinks.iterrows():
	driver.get(row['TrackerLink'])
	time.sleep(3)

	try:
		error = driver.find_element(By.XPATH,"//h1[text() = '404']")
		row['Error'] = 'InvalidLink'

	except NoSuchElementException:

		try:
			error = driver.find_element(By.XPATH,"//*[@class='lead' and contains(text(),'This profile is private.')]")
			row['Error'] = 'PrivateProfile'

		except NoSuchElementException:
			print("profile should be good")

	else:
		print("we chillin")


TwitchTrackerLinks.to_csv('LoadFiles/TwitchUsernameTrackerLink.csv')

driver.close()
