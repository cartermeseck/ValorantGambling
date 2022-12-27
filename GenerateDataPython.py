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


def load_files():
    AgentFinalList = pd.read_csv('FinalAgentList.csv')
    MapList = pd.read_csv('MapList.csv')
    agentLinkList = pd.read_csv('agentLinkList.csv')
    AgentMapList = pd.read_csv('AgentMapComboList.csv')
    AgentMapList = AgentMapList.assign(WinPct = 0, Matches = 0)
    return AgentFinalList,MapList,agentLinkList,AgentMapList


#Return selenium element text (used for multithreading)
def element_text(element):
    return element.text    


#Return selenium element src (used for multithreading)
def element_src(element):
    return element.get_attribute("src")   


#Function to click the loadmore button to load more matches
def click_loadmore_button(window, driver):

    for i in range(23):

        try:

            #Scroll to bottom of webpage
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #obtain button element
            button = WebDriverWait(driver,6).until(EC.visibility_of_element_located((By.XPATH,"//button[text()=' Load More Matches ']")))

            #Click button
            button.click()

            #Wait a second
            time.sleep(1)
            
        except:
            print("No loadmore button found, most likely an error with how many times you are pressing the button")
            return


#Main function for generating everything.
def generateData(trackerLink):


    # Load data of Agent, Map, and Links to profiles of streamers.
    AgentFinalList,MapList,agentLinkList,AgentMapList = load_files()



    #PROGRAM NOTE FOR FUTURE
    #Would be cool to make this connect to a SQL server so the dataset can be easily updated by multiple people, without having to manually download a new csv file





    #Intialize webdriver (webpage)
    driver = webdriver.Chrome()

    #Navigate to inputted persons tracker profile
    driver.get(trackerLink)

    #Wait for webpage to load fully before running scripts
    time.sleep(7)


    #get current window
    window = driver.current_window_handle
    
    
    #Click button while it is on the page, and as many times as can do before the time is up (3 minutes)
    #Note that it can't really be clicked on for 3 minutes, because that leaves no time to then get the text/src of each element
    click_loadmore_button(window,driver)





    #Intialize empty arrays for each element that I want the text/src of

    #Initialize empty array to append each matches map name to the array for later analysis
    map_names = None

    #Initialize empty array to append each matches map name to the array for later analysis
    agent_names = None

    #Initialize empty array to append each matches won rounds to the array for later analysis
    scoreWonList = None

    #Initialize empty array to append each matches lost rounds to the array for later analysis
    scoreLostList = None





    #Find the elements I want

    #Find Map names for each match
    maps = driver.find_elements(By.CLASS_NAME,"match__name")


    #Find Agent names for each match
    agents = driver.find_elements(By.XPATH,"//div[@class = 'match__portrait']//img")


    #Gets each matches rounds won element
    scoreWon = driver.find_elements(By.CLASS_NAME,"score--won")


    #Gets each matches rounds lost element
    scoreLost = driver.find_elements(By.CLASS_NAME,"score--lost")






    #Cool multithread stuff to append text for each element in scoreWon to scoreWonList
    with ThreadPoolExecutor(max_workers = 3) as executor:
        map_names = executor.map(element_text,maps)
        agent_names = executor.map(element_src,agents)
        scoreWonList = executor.map(element_text,scoreWon)
        scoreLostList = executor.map(element_text, scoreLost)



    #Get Player Username
    player = driver.find_element(By.CLASS_NAME,"trn-ign__username")
    playerUsername = player.text

    time.sleep(2)
    driver.close()


    #Load AgentMapComboList, as it is the main template for output.
    


    agent_names = pd.DataFrame(agent_names, columns = ["agent_names"])


    playerName = pd.DataFrame([playerUsername], columns = ["Username"])


    #Win/Lose extra

    scoreLostList2 = pd.DataFrame(scoreLostList, columns=["scoreLostList"])
    scoreWonList2 = pd.DataFrame(scoreWonList, columns=["scoreWonList"])

    
    df = pd.concat([scoreWonList2,scoreLostList2], axis = 1)


    df['scoreWonList'] = pd.to_numeric(df['scoreWonList'])
    df['scoreLostList'] = pd.to_numeric(df['scoreLostList'])

    df = df.assign(WinOrLose="ERROR")


    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():

        # Access the values in the 'ScoreWonList' and 'scoreLostList' columns
        roundsWon = row['scoreWonList']
        roundsLost = row['scoreLostList']

        # Compare the values and assign the result
        if roundsWon > roundsLost:
            df.at[index,'WinOrLose'] = "Win"
        elif roundsWon < roundsLost:
            df.at[index,'WinOrLose'] = "Lose"
        else:
            df.at[index,'WinOrLose'] = "Draw"
    


    #Agents

    agent_names2 = pd.DataFrame(agent_names)

    for index, row in agent_names2.iterrows():
        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        if row['agent_names'] == agentLinkList.loc[0, 'Jett']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Jett'


        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        if row['agent_names'] == agentLinkList.loc[0, 'Chamber']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Chamber'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Astra']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Astra'


        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Breach']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Breach'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Brimstone']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Brimstone'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Cypher']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Cypher'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Fade']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Fade'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Killjoy']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Killjoy'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Neon']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Neon'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Omen']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Omen'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Phoenix']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Phoenix'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Raze']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Raze'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Reyna']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Reyna'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Sage']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Sage'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Skye']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Skye'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Sova']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Sova'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Viper']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Viper'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Yoru']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Yoru'

        #Check if the value in the 'agent_names' column is present in the 'Jett' column of agentLinkList
        elif row['agent_names'] == agentLinkList.loc[0, 'Kayo']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Kayo'

        elif row['agent_names'] == agentLinkList.loc[0, 'Harbor']:
            # If it is, replace the value with 'Jett'
            agent_names2.loc[index, 'agent_names'] = 'Harbor'



    #Maps

    map_list = pd.DataFrame(map_names, columns = ["map_list"])

    

    WinLose = pd.DataFrame((df['WinOrLose']))

    AgentMapIndex = []

    output = pd.concat([playerName,WinLose,agent_names2,map_list], axis = 1)
    output['Username'] = playerUsername

    output = output.loc[(output['WinOrLose'] == "Win") | (output['WinOrLose'] == "Lose")]


    for i in range(0, AgentFinalList.shape[0]):
        agentIndex = output[(output['agent_names']) == (AgentFinalList.at[i,"Agent"])]
        agentIndex = (agentIndex.index).tolist()

        

        if len(agentIndex) > 0:
            for j in range(0, MapList.shape[0]):
                map_index = output[(output['map_list']) == MapList.at[j,"Map"]]
                map_index = (map_index.index).tolist()

                if(len(map_index) > 0):
                
                    combinedIndex = [x for x in agentIndex if x in map_index]

                    

                    agent = AgentFinalList.at[i,"Agent"]

                    

                    map_ = MapList.at[j,"Map"]

                    
                    
                    AgentMapIndex = AgentMapList.loc[(AgentMapList['Agent'] == agent) & (AgentMapList["Map"] == map_)].index

                    AgentMapIndex = AgentMapIndex.tolist()
                    

                    if (len(combinedIndex) > 0) and ("Win" in output.loc[combinedIndex,"WinOrLose"].values):

                        indices = output.index[output['WinOrLose'] == 'Win']

                        win_count = len((indices.intersection(combinedIndex)).tolist())

                        
                        win_pct = win_count / len(combinedIndex)
                        AgentMapList.loc[AgentMapIndex,"WinPct"] = win_pct
                        AgentMapList.loc[AgentMapIndex,"Matches"] = len(combinedIndex)

                    elif (len(combinedIndex) > 0) and ("Win" not in output.loc[combinedIndex,"WinOrLose"].values):
                        AgentMapList.loc[AgentMapIndex,"Matches"] = len(combinedIndex)

    AgentMapList = pd.concat([playerName,AgentMapList], axis = 1)
    AgentMapList['Username'] = playerUsername
    AgentMapList = AgentMapList.sort_values(by = 'Matches', ascending = False)

    return(AgentMapList)



#Load links to each persons profile
TwitchTrackerLinks = pd.read_csv('TwitchUsernameTrackerLink.csv')

for index, row in TwitchTrackerLinks.iterrows():
    newDataFrame = generateData(row['TrackerLink'])
    outputName = row['TwitchName']
    newDataFrame.to_csv(outputName + '.csv')
