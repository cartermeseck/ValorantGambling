from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By


#Main function for generating everything.


def generateData(trackerLink):


    # Load data of Agent, Map, and Links to profiles of streamers.

    #PROGRAM NOTE FOR FUTURE
    #Would be cool to make this connect to a SQL server so the dataset can be easily updated by multiple people, without having to manually download a new csv file

    global AgentFinalList
    global MapList
    global AgentMapList
    global agentLinkList

    driver = webdriver.Chrome()
    driver.get(trackerLink)
    time.sleep(5)
    # Get the button element
    button = driver.find_element(By.XPATH, "//button[text()=' Load More Matches ']")

    #PROGRAM NOTE IF PROBLEMS!
    # Keep clicking the load more matches button as long as it exists (COULD CAUSE PROBLEMS IF THERE ARE A TON OF MATCHES, BECAUSE YOU HAVE A TIMER UNTIL PAGE REFRESHES!)
    """
    while button.is_displayed():
    	window = driver.current_window_handle
    	# Execute JavaScript code to scroll to the bottom of the page
    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    	button.click()
    	time.sleep(5)

    """
    window = driver.current_window_handle
    # Execute JavaScript code to scroll to the bottom of the page
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #button.click()
    #time.sleep(5)

    #Find Map names for each match
    maps = driver.find_elements(By.CLASS_NAME,"match__name")

    #Initialize empty array to append each matches map name to the array for later analysis
    map_names = []

    #Append each matches map to array
    for element in maps:
        map_names.append(element.text)
        

    

	#Find Agent names for each match
    agents = driver.find_elements(By.XPATH,"//div[@class = 'match__portrait']//img")

    
    #Initialize empty array to append each matches map name to the array for later analysis
    agent_names = []

    #Append each matches map to array
    for element in agents:
    	agent_names.append(element.get_attribute("src"))

    agent_names = pd.DataFrame(agent_names, columns = ["agent_names"])


    
    #Find Score of each match (To calculate if it was a win, loss, or draw)

    #Gets each matches rounds won element
    scoreWon = driver.find_elements(By.CLASS_NAME,"score--won")

    #Initialize empty array to append each matches won rounds to the array for later analysis
    scoreWonList = []

    #Gets eatch matches rounds lost element
    scoreLost = driver.find_elements(By.CLASS_NAME,"score--lost")

    #Initialize empty array to append each matches lost rounds to the array for later analysis
    scoreLostList = []

    #Append each matches rounds won to array
    for element in scoreWon:
    	scoreWonList.append(element.text)

	#Append each matches rounds lost to array
    for element in scoreLost:
    	scoreLostList.append(element.text)



    #Get Player Username
    player = driver.find_element(By.CLASS_NAME,"trn-ign__username")
    playerUsername = player.text
    playerName = pd.DataFrame([playerUsername], columns = ["Username"])


    driver.close()

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
                        #win_count = len([i for i in range(len(combinedIndex)) if output[combinedIndex[i]]["WinOrLose"] == "Win"])

                        
                        win_count = (len((output.loc[combinedIndex,"WinOrLose"]).index))

                        win_pct = win_count / len(combinedIndex)
                        AgentMapList.loc[AgentMapIndex,"WinPct"] = win_pct
                        AgentMapList.loc[AgentMapIndex,"Matches"] = len(combinedIndex)

                    elif (len(combinedIndex) > 0) and ("Win" not in output.loc[combinedIndex,"WinOrLose"].values):
                        AgentMapList.loc[AgentMapIndex,"Matches"] = len(combinedIndex)



    AgentMapList = pd.concat([playerName,AgentMapList], axis = 1)
    AgentMapList['Username'] = playerUsername
    AgentMapList = AgentMapList.sort_values(by = 'Matches', ascending = False)

    return(AgentMapList)
    


AgentFinalList = pd.read_csv('FinalAgentList.csv')

MapList = pd.read_csv('MapList.csv')

AgentMapList = pd.read_csv('AgentMapComboList.csv')

AgentMapList = AgentMapList.assign(WinPct = 0, Matches = 0)

agentLinkList = pd.DataFrame(columns = ['Jett','Kayo','Chamber'], index = range(1))

agentLinkList['Jett'] = "https://titles.trackercdn.com/valorant-api/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png"
agentLinkList['Kayo'] = "https://titles.trackercdn.com/valorant-api/agents/601dbbe7-43ce-be57-2a40-4abd24953621/displayicon.png"
agentLinkList['Chamber'] = "https://titles.trackercdn.com/valorant-api/agents/22697a3d-45bf-8dd7-4fec-84a9e28c69d7/displayicon.png"
agentLinkList['Astra'] = "https://titles.trackercdn.com/valorant-api/agents/41fb69c1-4189-7b37-f117-bcaf1e96f1bf/displayicon.png"
agentLinkList['Breach'] = "https://titles.trackercdn.com/valorant-api/agents/5f8d3a7f-467b-97f3-062c-13acf203c006/displayicon.png"
agentLinkList['Brimstone'] = "https://titles.trackercdn.com/valorant-api/agents/9f0d8ba9-4140-b941-57d3-a7ad57c6b417/displayicon.png"
agentLinkList['Cypher'] = "https://titles.trackercdn.com/valorant-api/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png"
agentLinkList['Fade'] = "https://titles.trackercdn.com/valorant-api/agents/dade69b4-4f5a-8528-247b-219e5a1facd6/displayicon.png"
agentLinkList['Killjoy'] = "https://titles.trackercdn.com/valorant-api/agents/1e58de9c-4950-5125-93e9-a0aee9f98746/displayicon.png"
agentLinkList['Neon'] = "https://titles.trackercdn.com/valorant-api/agents/bb2a4828-46eb-8cd1-e765-15848195d751/displayicon.png"
agentLinkList['Omen'] = "https://titles.trackercdn.com/valorant-api/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png"
agentLinkList['Phoenix'] = "https://titles.trackercdn.com/valorant-api/agents/eb93336a-449b-9c1b-0a54-a891f7921d69/displayicon.png"
agentLinkList['Raze'] = "https://titles.trackercdn.com/valorant-api/agents/f94c3b30-42be-e959-889c-5aa313dba261/displayicon.png"
agentLinkList['Reyna'] = "https://titles.trackercdn.com/valorant-api/agents/a3bfb853-43b2-7238-a4f1-ad90e9e46bcc/displayicon.png"
agentLinkList['Sage'] = "https://titles.trackercdn.com/valorant-api/agents/569fdd95-4d10-43ab-ca70-79becc718b46/displayicon.png"
agentLinkList['Skye'] = "https://titles.trackercdn.com/valorant-api/agents/6f2a04ca-43e0-be17-7f36-b3908627744d/displayicon.png"
agentLinkList['Sova'] = "https://titles.trackercdn.com/valorant-api/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/displayicon.png"
agentLinkList['Viper'] = "https://titles.trackercdn.com/valorant-api/agents/707eab51-4836-f488-046a-cda6bf494859/displayicon.png"
agentLinkList['Yoru'] = "https://titles.trackercdn.com/valorant-api/agents/7f94d92c-4234-0a36-9646-3a87eb8b5c89/displayicon.png"
agentLinkList['Harbor'] = "https://titles.trackercdn.com/valorant-api/agents/…78ed7-4637-86d9-7e41-71ba8c293152/displayicon.png"







TwitchTrackerLinks = pd.read_csv('TwitchUsernameTrackerLink.csv')


for index, row in TwitchTrackerLinks.iterrows():
    newDataFrame = generateData(row['TrackerLink'])
    outputName = row['TwitchName']
    newDataFrame.to_csv(outputName + '.csv')



#newDataFrame = (generateData("https://tracker.gg/valorant/profile/riot/SEN%20zekken%235193/matches?playlist=competitive"))
#newDataFrame.to_csv('output.csv', index=True)





