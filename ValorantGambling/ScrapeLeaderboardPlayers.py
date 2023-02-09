from selenium import webdriver
import time
import pandas as pd
import numpy as np
import itertools
from urllib.parse import urlparse, urlunparse

from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options

#Not used currently, but could be useful later, possibly in click_loadmore_button
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ast

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from sklearn.naive_bayes import GaussianNB
#Return selenium element text (used for multithreading)
def element_text(element):
    return element.text    


#Return selenium element src (used for multithreading)
def element_src(element):
    return element.get_attribute("src")  


def element_href(element):
    return element.get_attribute("href")  


def scrapeTop100(driver,link, region):

	driver.get(link)


	#usernamesList = []
	#hashtagsList = []

	#Gets each player username element
	usernames = driver.find_elements(By.CLASS_NAME,"trn-ign__username")
	
	#for element in usernames:
		#usernamesList.append(element.text)

	#Gets each player hashtag element
	hashtags = driver.find_elements(By.CLASS_NAME,"trn-ign__discriminator")
		
	#for element in hashtags:
		#hashtagsList.append(element.text)


	with ThreadPoolExecutor() as executor:
		usernamesList = executor.map(element_text,usernames)
		hashtagsList = executor.map(element_text,hashtags)


	usernamesList = [username for username in usernamesList]
	hashtagsList = [hashtag for hashtag in hashtagsList]


	usernamesList = pd.DataFrame(usernamesList, columns = ['Usernames'])
	hashtagsList = pd.DataFrame(hashtagsList, columns = ['Hashtags'])

	playerList = pd.concat((usernamesList,hashtagsList), axis = 1)
	playerList['Region'] = region


	return playerList


def getMatchLinks(link):
	driver = webdriver.Chrome()
	#print('itermation check 1')
	driver.get(link)
	#print('itermation check 2')

	#Initialize empty array to append each matches map name to the array for later analysis
	match = []


	#Gets each player match link element
	wait = WebDriverWait(driver,10)
	try:
		#print('itermation check 3')
		wait.until(EC.presence_of_element_located((By.XPATH,"//a[@class='match__link']")))
		#print('itermation check 4')
		matches = driver.find_elements(By.XPATH,"//a[@class='match__link']")
		#print('itermation check 5')
		match = list(map(element_href,matches))
	except:
		print("Timed out waiting for matches to load on page")

	#Cool multithread stuff to append text for each element in scoreWon to scoreWonList
	#with ThreadPoolExecutor() as executor:
		#match = list(executor.map(element_href,matches))
	#print('itermation check 6')

	#driver.close()
	return pd.DataFrame(match,columns = ['MatchLinks'])



def removeMatchPlayer(url):
	# Parse the URL and get the query string
	parsed_url = urlparse(url)

	trimmed_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

	return trimmed_url


def agentLink(link):

	agent = agentLinks_dict.get(link)

	if agent is None:
		return None
	else:
		return agent


agents_df = pd.read_csv('newAgentLinkList.csv')

agentLinks_dict = {}

for index, row in agents_df.iterrows():
	agentLinks_dict[row['Link']] = row['Agent']


def getMatchData(driver,link):

	#driver = webdriver.Chrome()
	#print("getting linnk")
	driver.get(link)
	#print("got link")
	wait = WebDriverWait(driver,10)

	try:
		wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class = 'trn-match-drawer__header-value valorant-color-team-1']")))
	except:
		print("webpage didn't load properly")
		return

	match_df = pd.DataFrame(columns = ['Map','WinGame','WinPistol','AgentsTeam1','AgentsTeam2'])

	teamAScore = int(driver.find_element(By.XPATH, "//div[@class = 'trn-match-drawer__header-value valorant-color-team-1']").text)

	teamBScore = int(driver.find_element(By.XPATH, "//div[@class = 'trn-match-drawer__header-value valorant-color-team-2']").text)




	if teamAScore == teamBScore:
		match_df.at[0,'WinGame'] = 'Draw'
		return
	elif teamAScore > teamBScore:
		match_df.at[0,'WinGame'] = 'TeamA'
	elif teamAScore < teamBScore:
		match_df.at[0,'WinGame'] = 'TeamB'



	wait.until(EC.presence_of_element_located((By.XPATH,"//img[contains(@src, 'https://titles.trackercdn.com/valorant-api/agents/')]")))

	agents = driver.find_elements(By.XPATH,"//img[contains(@src, 'https://titles.trackercdn.com/valorant-api/agents/')]")
	
	winFirst = "none"

	try:
		winFirst = element_src(driver.find_element(By.XPATH,"//div[@class = 'entry']//img[contains(@src,'https://trackercdn.com/cdn/tracker.gg/valorant/icons')]"))
	except:
		print("something fucked up loading who wins each round")


	if "win1.png" in winFirst:
		match_df.at[0,'WinPistol'] = 'TeamA'
	elif "win1.png" not in winFirst:
		match_df.at[0,'WinPistol'] = 'TeamB'
	else:
		match_df.at[0,'WinPistol'] = 'Error'



	agentsTeamA = [agentLink(element_src(element)) for element in agents[:5]]
	agentsTeamB = [agentLink(element_src(element)) for element in agents[5:]]

	
	mapPlayed = driver.find_element(By.CLASS_NAME, "trn-match-drawer__header-value").text

	match_df.at[0,'Map'] = mapPlayed
	
	match_df.at[0,'AgentsTeam1'] = agentsTeamA
	match_df.at[0,'AgentsTeam2'] = agentsTeamB

	return match_df



def process_matches_for_machinelearning():
	matchList = pd.read_csv('MatchData.csv')
	matchList = pd.get_dummies(matchList,columns = ['Map'])

	matchList[['TeamA_Agent_Jett', 'TeamA_Agent_Kayo', 'TeamA_Agent_Chamber', 'TeamA_Agent_Astra', 'TeamA_Agent_Breach', 'TeamA_Agent_Brimstone', 'TeamA_Agent_Cypher', 'TeamA_Agent_Fade', 'TeamA_Agent_Killjoy', 'TeamA_Agent_Neon', 'TeamA_Agent_Omen', 'TeamA_Agent_Phoenix', 'TeamA_Agent_Raze', 'TeamA_Agent_Reyna', 'TeamA_Agent_Sage', 'TeamA_Agent_Skye', 'TeamA_Agent_Sova', 'TeamA_Agent_Viper', 'TeamA_Agent_Yoru', 'TeamA_Agent_Harbor','TeamB_Agent_Jett', 'TeamB_Agent_Kayo', 'TeamB_Agent_Chamber', 'TeamB_Agent_Astra', 'TeamB_Agent_Breach', 'TeamB_Agent_Brimstone', 'TeamB_Agent_Cypher', 'TeamB_Agent_Fade', 'TeamB_Agent_Killjoy', 'TeamB_Agent_Neon', 'TeamB_Agent_Omen', 'TeamB_Agent_Phoenix', 'TeamB_Agent_Raze', 'TeamB_Agent_Reyna', 'TeamB_Agent_Sage', 'TeamB_Agent_Skye', 'TeamB_Agent_Sova', 'TeamB_Agent_Viper', 'TeamB_Agent_Yoru', 'TeamB_Agent_Harbor']] = 0
	#refinedMatchData = pd.DataFrame(columns = ['Ascent','Bind','Breeze','Fracture','Haven','Icebox','Split','Pearl','WinGame','WinPistol','TeamA_Agent_Jett', 'TeamA_Agent_Kayo', 'TeamA_Agent_Chamber', 'TeamA_Agent_Astra', 'TeamA_Agent_Breach', 'TeamA_Agent_Brimstone', 'TeamA_Agent_Cypher', 'TeamA_Agent_Fade', 'TeamA_Agent_Killjoy', 'TeamA_Agent_Neon', 'TeamA_Agent_Omen', 'TeamA_Agent_Phoenix', 'TeamA_Agent_Raze', 'TeamA_Agent_Reyna', 'TeamA_Agent_Sage', 'TeamA_Agent_Skye', 'TeamA_Agent_Sova', 'TeamA_Agent_Viper', 'TeamA_Agent_Yoru', 'TeamA_Agent_Harbor','TeamB_Agent_Jett', 'TeamB_Agent_Kayo', 'TeamB_Agent_Chamber', 'TeamB_Agent_Astra', 'TeamB_Agent_Breach', 'TeamB_Agent_Brimstone', 'TeamB_Agent_Cypher', 'TeamB_Agent_Fade', 'TeamB_Agent_Killjoy', 'TeamB_Agent_Neon', 'TeamB_Agent_Omen', 'TeamB_Agent_Phoenix', 'TeamB_Agent_Raze', 'TeamB_Agent_Reyna', 'TeamB_Agent_Sage', 'TeamB_Agent_Skye', 'TeamB_Agent_Sova', 'TeamB_Agent_Viper', 'TeamB_Agent_Yoru', 'TeamB_Agent_Harbor'])
	matchList['AgentsTeam1'] = matchList['AgentsTeam1'].apply(ast.literal_eval)
	matchList['AgentsTeam2'] = matchList['AgentsTeam2'].apply(ast.literal_eval)
	refinedMatchData = matchList



	agentsTeamA = None
	agentsTeamB = None

	for index, row in matchList.iterrows():
		agentsTeamA = row['AgentsTeam1']
		agentsTeamB = row['AgentsTeam2']

		if row['WinGame'] == 'TeamA':
			refinedMatchData.at[index,('WinGame')] = 1
		elif row['WinGame'] == 'TeamB':
			refinedMatchData.at[index,('WinGame')] = 0

		for item in agentsTeamA:
			refinedMatchData.at[index,('TeamA_Agent_' + item)] = 1

		for item in agentsTeamB:
			refinedMatchData.at[index,('TeamB_Agent_' + item)] = 1

			
		
	return refinedMatchData.drop(columns = ['AgentsTeam1','AgentsTeam2','WinPistol'])


import matplotlib

def machine_learning_matches(matches):

	# Load the data and split into training and test sets
	#matches = pd.read_csv('ValorantMatches.csv', index_col = 0)

	
	X = matches.drop(columns=['WinGame'])
	y = matches['WinGame']

	
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

	# Scale the data
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.transform(X_test)

	# Create a logistic regression model
	logreg = LogisticRegression()

	# Fit the model on the scaled training data
	logreg.fit(X_train_scaled, y_train)

	# Make predictions on the scaled test data
	y_pred = logreg.predict(X_test_scaled)

	accuracy = accuracy_score(y_test, y_pred)

	print("Accuracy using logistic regression")
	print(accuracy)

	

	'''
	matches = pd.read_csv('Testingstuffss.csv', index_col = 0)
	X = matches.drop(columns=['WinGame'])
	y = matches['WinGame']
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	# Create a logistic regression model
	logreg = LogisticRegression()

	# Fit the model on the training data
	logreg.fit(X_train, y_train)

	# Make predictions on the test data
	y_pred = logreg.predict(X_test)

	accuracy = accuracy_score(y_test, y_pred)

	print("Accuracy using logistic regression")
	print(accuracy)

	# Create a decision tree classifier
	dt = DecisionTreeClassifier()

	# Fit the model on the training data
	dt.fit(X_train, y_train)

	# Make predictions on the test data
	y_pred = dt.predict(X_test)

	accuracy = accuracy_score(y_test, y_pred)

	print("Accuracy using decision trees")
	print(accuracy)
	'''


#process_matches_for_machinelearning()

#(process_matches_for_machinelearning()).to_csv("Testingstuffss.csv")

#machine_learning_matches()


matches = pd.read_csv("ValorantMatches.csv", index_col = 0)

#print(matches.columns.values[28:48])
 
print(matches.shape[0])


team_a_columns = matches.columns[8:28]
team_b_columns = matches.columns[28:48]
df_deduped = matches.drop_duplicates(subset=team_a_columns.tolist() + team_b_columns.tolist())




print("before drop")
machine_learning_matches(matches)


print("Afer drop")
machine_learning_matches(df_deduped)


'''
Matches_to_process = pd.read_csv('NewProcessedMatches.csv')


chrome_options = Options()
chrome_options.add_extension('LoadFiles/3.15.2_0.crx')

driver = webdriver.Chrome(options = chrome_options)

#Wait for webpage to load fully before running scripts
time.sleep(5)

#get current window
window = driver.current_window_handle

# Get a list of all open tabs
tabs = driver.window_handles

# Switch to the tab opened by the extension
driver.switch_to.window(tabs[0])

# Close the tab
driver.close()

# Switch back to the main tab
driver.switch_to.window(tabs[1])



MatchData = pd.DataFrame(columns = ['Map','WinGame','WinPistol','AgentsTeam1','AgentsTeam2'])

pizza = 1
for index, row in Matches_to_process.iterrows():

	if pizza == 100:
		break
	#print("calling concat shit")
	MatchData = pd.concat((MatchData,(getMatchData(driver,row['MatchLinks']))))
	pizza+=1

driver.close()
print(MatchData)
#MatchData.to_csv("MatchData.csv")

'''







#print(agentLink("https://titles.trackercdn.com/valorant-api/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png"))


'''
	wait = WebDriverWait(driver,10)
	wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class = 'image']//div[@class = 'st__item st-content__item-value st__item--sticky st__item--wide st-custom-name st-entry-party st-entry-party--1']//img")))
	#print('itermation check 4')

	matches = driver.find_elements(By.XPATH,"//div[@class = 'image']//img")
	#print('itermation check 5')
	match = list(map(element_src,matches))
	print(match)
'''

#getMatchData()

'''

#Initialize webpage
chrome_options = Options()
chrome_options.add_extension('LoadFiles/3.15.2_0.crx')

driver = webdriver.Chrome(options = chrome_options)

#Wait for webpage to load fully before running scripts
time.sleep(5)

#get current window
window = driver.current_window_handle

# Get a list of all open tabs
tabs = driver.window_handles

# Switch to the tab opened by the extension
driver.switch_to.window(tabs[0])

# Close the tab
driver.close()

# Switch back to the main tab
driver.switch_to.window(tabs[1])
'''



'''
TopNAPlayerNames = scrapeTop100(driver,'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=na', 'NorthAmerica')
TopEUPlayerNames = scrapeTop100(driver,'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=eu', 'Europe')
TopAPACPlayerNames = scrapeTop100(driver,'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=ap', 'Asia-Pacific')
TopKoreaPlayerNames = scrapeTop100(driver,'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=kr', 'Korea')
TopBrazilPlayerNames = scrapeTop100(driver,'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=br', 'Brazil')
TopLATAMPlayerNames = scrapeTop100(driver,'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=latam', 'LatinAmerica')

GlobalPlayerTop100 = pd.concat([TopNAPlayerNames,TopEUPlayerNames,TopAPACPlayerNames,TopKoreaPlayerNames,TopBrazilPlayerNames,TopLATAMPlayerNames], ignore_index = True)

GlobalPlayerTop100.to_csv("GlobalPlayerTop100.csv")
'''

'''
Matches = pd.DataFrame(columns = ['MatchLinks'])

GlobalPlayerTop100 = pd.read_csv('GlobalPlayerTop100.csv')

for index, row in GlobalPlayerTop100.iterrows():

	row['Hashtags'] = row['Hashtags'].replace("#","")

	#MatchList = getMatchLinks(driver,'https://tracker.gg/valorant/profile/riot/' + row['Usernames'] + '%23' + row['Hashtags'] + '/matches?playlist=competitive')
	#MatchLinks = pd.DataFrame(MatchList, columns = ['MatchLinks'])
	#Matches = pd.concat([Matches,MatchLinks],ignore_index = True)
	print(row['Usernames'] + row['Region'])

	Matches = pd.concat((Matches,(getMatchLinks('https://tracker.gg/valorant/profile/riot/' + row['Usernames'] + '%23' + row['Hashtags'] + '/matches?playlist=competitive'))))


Matches.to_csv("PreprocessedMatches.csv")



for index, row in Matches.iterrows():
	Matches.at[index,'MatchLinks'] = removeMatchPlayer(row['MatchLinks'])

Matches.to_csv('ProcessedMatchLinks.csv')
'''



