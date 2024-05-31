import requests;

# summonerName = input("Welcome to the mini-desktop match tracker for League of Legends! Please enter your summoner name:")
# tagline = input("What is your tagline?: ")
# region = input("What region are you in?(enter americas for testing purposes): ")
summonerName = 'serpentshadow299'
tagline = 'NA1'
region = 'americas'

api_key = "RGAPI-0294496c-12d8-4ecd-a7d1-3bb8226c5d5d"
api_key_addon = "?api_key=" + api_key

api_user_url = "https://" + region + ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + summonerName + "/" + tagline + api_key_addon
response = requests.get(api_user_url)
userInfo = response.json()
userPUUID = userInfo['puuid']

# api_summoner_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + userPUUID + api_key_addon
# response2 = requests.get(api_summoner_url)
# info = response2.json()
# print(info['summonerLevel'])

api_matches_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + userPUUID + "/ids?start=0&count=20&api_key=" + api_key
# print (api_matches_url)
response = requests.get(api_matches_url)
matchData = response.json()
# print(matchData)
match_id = matchData[0]


def get_match_data(region, match_id):
    api_url = (
        "https://" + 
        region + 
        ".api.riotgames.com/lol/match/v5/matches/" + 
        match_id + 
        api_key_addon
    )
    response = requests.get(api_url)
    data = response.json()
    return data

def findPlayerNumber(match_data):
    num = 0
    while(num<=9):
        if(match_data['metadata']['participants'][num]== userPUUID):
            return num
        num = num + 1

def create_match_header(match_data):
    playerNumber = findPlayerNumber(match_data)
    return ("----------------------------\n" + 
            "Champion Played: " + match_data['info']['participants'][playerNumber]['championName'] + "\n" +
            "Match Length:" + ("%.2f" %(match_data['info']['gameDuration']/60)) + "\n"
            "End Result: " + ("Win" if match_data['info']['participants'][playerNumber]['win'] else "Loss") + 
            "\n----------------------------\n"
        )

print(create_match_header(get_match_data(region, match_id)))

print("Here is some of the data from your past 20 games!: ")

for x in range(20):
    match_id = matchData[x]
    print(create_match_header(get_match_data(region, match_id)))
