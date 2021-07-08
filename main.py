import requests
import json
import csv
import os
import math
import re
from hltbapi import HtmlScraper
import datetime  ##########use timeit

os.getcwd()

if __name__ == '__main__':
    begin_time = datetime.datetime.now()  ###########
    # Regex of keywords for HLTB game name search
    keyWords = 'Single Player|Multi-Player|Multiplayer|&|:|-|Steam|The|Edition|Deluxe|Premium|Complete|HD|Definitive|Anniversary|Enhanced|\|\(.*\)'


    # Export file to JSON
    def exportJSON(file, name):
        with open(name + '_data.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(file, jsonfile, ensure_ascii=False, indent=4)


    # Return review numbers of owned STEAM games
    def getGameReviews(gameID):
        gameReviews = (requests.get('https://store.steampowered.com/appreviews/'
                                    + gameID
                                    + '?json=1&language=all&purchase_type=all').json())  # &review_type=positive
        totalVotes = gameReviews['query_summary']['total_reviews']
        if totalVotes == 0:
            return 0, 0, 0, 0, 0
        else:
            totalPositive = gameReviews['query_summary']['total_positive']
            totalNegative = gameReviews['query_summary']['total_negative']
            reviewScore = totalPositive / totalVotes
            rating = reviewScore - (reviewScore - 0.5) * math.pow(2, - math.log10(totalVotes + 1))
            return totalVotes, totalPositive, totalNegative, (round(reviewScore * 100)), (round(rating * 100))


    # Scrap expected game length times per play style from How Long to Beat website
    def getHowLongToBeat(name):
        # Using checklist to check steam name searches in HLTB base
        # Using regex to exclude mismatches between steam and HLTB game names
        name = re.sub(keyWords, ' ', name)
        # Remove utf-8 coded text for better search results
        encodeName = name.encode(encoding='ascii', errors='ignore')
        decodeName = encodeName.decode()
        try:
            howLongToBeat = HtmlScraper().search(decodeName)[0]
            # gameLengths = howLongToBeat.gameplayMain, howLongToBeat.gameplayMainExtra, howLongToBeat.gameplayCompletionist
            # print(decodeName + ' -> ' + howLongToBeat.gameName)
            return round(howLongToBeat.gameplayMain), round(howLongToBeat.gameplayMainExtra), \
                   round(howLongToBeat.gameplayCompletionist), decodeName + ' -> ' + howLongToBeat.gameName
        except:
            print("ERROR! ITEM NOT FOUND -> " + decodeName)
            # checkList.append("ERROR -> " + decodeName)
            return 'Error', 'Error', 'Error', decodeName + ' -> NOT FOUND!'


    # To return owned games in STEAM form the URL with the following strings
    steamLink = 'http://api.steampowered.com/'
    ownedGames = 'IPlayerService/GetOwnedGames/v1?'
    # Put in your Steam Key
    steamKey = '&key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    # Put in your Steam ID
    steamID = '&steamid=XXXXXXXXXXXXXXXXX'
    textFormat = '&format=json'
    appInfo = '&include_appinfo=True'
    freeGames = '&include_played_free_games=True'

    # Return owned STEAM games list
    getOwnedGames = (requests.get(steamLink + ownedGames + steamKey + steamID + textFormat + appInfo
                                  + freeGames)).json()
    exportJSON(getOwnedGames, name='owned_games_steam')

    # Get the total count of Steam games
    gamesTotal = ["Total Steam game count: " + str(getOwnedGames['response']['game_count'])]
    rowTags = ['count', 'ID', 'Game Name', 'Steam Playtime(h)', 'Main Story(h)', 'Extra content(h)', 'Complete(h)',
               'Total Votes', 'Total Positive', 'Total Negative', 'Score(%)', 'Steam db Score(%)']

    # Get the game IDs, names, total playtime per title, total vote numbers, total positive and negative numbers
    gameItems = []
    checkList = []
    gameList = (getOwnedGames['response']['games'])
    oldCount = 0
    print("Going through the user's Steam library")
    for count, item in enumerate(gameList, 1):
        # Show the percentage of the list done
        newCount = int(count / len(gameList) * 100)
        if newCount != oldCount:
            oldCount = newCount
            print('List done: ' + str(newCount) + '%')

        story, extra, complete, gameName = getHowLongToBeat(name=(str(item['name'])))
        total, positive, negative, score, steamScore = getGameReviews(str(item['appid']))
        gameItems.append([count, item['appid'], item['name'], item['playtime_forever'],
                          story, extra, complete,
                          total, positive, negative, score, steamScore,
                          ])
        checkList.append(gameName)

    # Export to JSON file
    exportJSON((gamesTotal, gameItems), name='game_list')
    exportJSON(checkList, name='check_list')

    # Export to CSV file
    with open('game_list_data.csv', 'w', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(gamesTotal)
        writer.writerow(rowTags)
        writer.writerows(gameItems)

    # OPTIONAL: Get the Steam user and badge level
    steamLevel = 'IPlayerService/GetSteamLevel/v1?'
    badgeLevel = 'IPlayerService/GetBadges/v1?'

    getSteamLevel = requests.get(steamLink + steamLevel + steamID + steamKey)
    getBadgeLevel = requests.get(steamLink + badgeLevel + steamID + steamKey)
    exportJSON([getSteamLevel.json(), getBadgeLevel.json()], name='user_level_steam')

    # OPTIONAL: Get recently played STEAM games
    recentlyPlayed = 'IPlayerService/GetRecentlyPlayedGames/v1?'

    getRecentlyPlayed = requests.get(steamLink + recentlyPlayed + steamID + steamKey)
    exportJSON(getRecentlyPlayed.json(), name='recently_played_steam')

    # OPTIONAL: Get game's Steam page details
    gamePageID = '12370'

    getGameDetails = requests.get('https://store.steampowered.com/api/appdetails?appids=' + gamePageID)
    exportJSON(getGameDetails.json(), name='game_details')

    print(datetime.datetime.now() - begin_time)  ########
