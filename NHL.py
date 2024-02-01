#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 11:46:24 2022

@author: vaihitareddy
"""

import pandas as pd
import numpy as np
import re
import requests
import matplotlib.pyplot as plt


def array_transpose(list):
    return np.array(list).reshape(len(list), 1)

def get_recent_data(data, name, num_games):
    index = np.where(data["Team"].values == name)[0]
    if len(index) < num_games:
        num = len(index)
    else:
        num = num_games
    index = index[:num]
    points_gained = np.zeros(len(index))
    points_lost = np.zeros(len(index))
    info = []
    for i in range(len(index)):
        date = str(data.iat[index[i], 0])
        date = date[:-2] + "." + date[-2:]
        points_gained[i] = data.iat[index[i], 7]
        if index[i] % 2 == 0:
            oppo_index = index[i] + 1
        else:
            oppo_index = index[i] - 1
        oppo = data.iat[oppo_index, 3]
        game_info = date + " " + oppo
        info.append(game_info)
        points_lost[i] = data.iat[oppo_index, 7]
    points_delta = points_gained - points_lost
    points_total = points_gained + points_lost 
    win = np.sum((points_delta > 0).astype(int)) / len(index)
    stat = np.zeros(len(index))
    stat = np.vstack((stat, points_gained, points_lost, 
                      points_delta, points_total))
    stat = stat[1:,:]
    return info, num, win, stat
#print(get_recent_data(merged, "Pittsburgh", 10))


def get_opponent_data(data, name, oppo):
    index = np.where(data["Team"].values == name)[0]
    points_gained = []
    points_lost = []
    points_delta = []
    count = 0
    for i in range(len(index)):
        if index[i] % 2 == 0:
            oppo_index = index[i] + 1
        else:
            oppo_index = index[i] - 1
        oppo_name = data.iat[oppo_index, 3]
        if oppo_name != oppo:
            continue
        else:
            points_gained.append(data.iat[index[i], 7])
            points_lost.append(data.iat[oppo_index, 7])
            count += 1
    points_gained = np.array(points_gained)
    points_lost = np.array(points_lost)
    points_delta = points_gained - points_lost
    points_total = points_gained + points_lost
    stat = np.zeros(count)
    stat = np.vstack((stat, points_gained, points_lost, 
                      points_delta, points_total))
    stat = stat[1:, :]
    win = np.sum((points_delta > 0).astype(int)) / count
    return win, stat

#print(get_opponent_data(merged, "Pittsburgh", "TampaBay")) 
  
def plot_1(games_info, number, game_records, number_of_games, teams_dict, team_name):
    x = np.array(games_info)
    x_fit = np.arange(number)
    l_1 = np.polyfit(x_fit, game_records[0], 1)
    l_2 = np.polyfit(x_fit, game_records[1], 1)
    l_3 = np.polyfit(x_fit, game_records[2], 1)
    l_4 = np.polyfit(x_fit, game_records[3], 1)
    p_1 = np.poly1d(l_1)
    p_2 = np.poly1d(l_2)
    p_3 = np.poly1d(l_3)
    p_4 = np.poly1d(l_4)
    plt.scatter(x, game_records[0], label = "Points Gained", c = "b")
    plt.scatter(x, game_records[1], label = "Points Lost", c = "r")
    plt.scatter(x, game_records[2], label = "Points Difference", c = "g")
    plt.scatter(x, game_records[3], label = "Points Sum", c = "y")
    plt.plot(x, p_1(x_fit), c = "b")
    plt.plot(x, p_2(x_fit), c = "r")
    plt.plot(x, p_3(x_fit), c = "g")
    plt.plot(x, p_4(x_fit), c = "y")
    plt.xlabel("Game Information")
    plt.xticks(rotation = 30, size = 6)
    plt.ylabel("Points")
    plt.yticks(np.arange(np.min(game_records[2]), np.max(game_records[3]), 10),rotation = 30, size = 6)
    plt.title(f"Gained and Lost Points within the Recent {number_of_games} Games of {teams_dict[team_name]}")
    plt.legend(loc = 1)                    
    plt.show()

def main():
# current data
    url = "https://sports.yahoo.com/nhl/odds/"
    tables = pd.read_html(url)
    number_tables = len(tables)
    teams_init = []
    moneyline = []
    
    
    for i in range(number_tables - 1):
        table = tables[i]
    
        teams_init.append(table.iat[0,0])
        teams_init.append(table.iat[1,0])
        if table.iat[0, 1] == "-":
            moneyline.append("NA")
        if table.iat[1, 1] == "-":
            moneyline.append("NA")
        else:
            moneyline.append(int(table.iat[0,1][-4:]))
            moneyline.append(int(table.iat[1,1][-4:]))
    
    teams = []
    for team in teams_init:
        if re.search(r"\(", team) != None:
            index = team.find("(")
        elif re.search(r"[0-9]*$", team) != None:
            number = re.findall(r"\d", team)
            index = team.find(number[0])
        teams.append(team[:index])
    # print(teams)
    
    
    teams = array_transpose(teams)
    moneyline = array_transpose(moneyline)
    
    
    dataset = np.zeros((len(teams), 1))
    dataset = np.hstack((dataset,teams, moneyline))
    dataset = dataset[:,1:]
    dataframe = pd.DataFrame(dataset)
    col_name = ["Team", "Moneyline"]
    dataframe.columns = col_name
    # print(dataframe)
    team_dict = {
                 "Boston": "Boston Bruins","Seattle": "Seattle Kraken",
                 "Vancouver" :"Vancouver Canucks",
                 "Buffalo": "Buffalo Sabres", "Detroit": "Detroit Red Wings",
                 "Florida": "Florida Panthers", "Montreal": "Montreal Canadiens",
                 "Ottawa": "Ottawa Senators", "TampaBay": "Tampa Bay Lightning",
                 "Toronto": "Toronto Maple Leafs", "Carolina": "Carolina Hurricanes",
                 "Columbus ": "Columbus Blue Jackets", "NewJersey": "New Jersey Devils",
                 "NYIslanders ": "New York Islanders", "NYRangers": "New York Rangers",
                 "Philadelphia": "Philadelphia Flyers", "Pittsburgh": "Pittsburgh Penguins",
                 "Washington": "Washington Capitals", "Arizona": "Arizona Coyotes",
                 "Chicago": "Chicago Blackhawks", "Colorado": "Colorado Avalanche",
                 "Dallas": "Dallas Stars", "Minnesota": "Minnesota Wild",
                 "Nashville": "Nashville Predators", "St.Louis": "St. Louis Blues",
                 "Winnipeg": "Winnipeg Jets" ,"Anaheim": "Anaheim Ducks",
                 "Calgary": "Calgary Flames", "Edmonton": "Edmonton Oilers",
                 "LosAngeles": "Los Angeles Kings	", "SanJose": "San Jose Sharks", "Vegas": "Vegas Golden Knights"
                 }
    
    region_dict = {
                 "Boston Bruins": "Boston","Seattle Kraken":"Seattle","Vancouver Canucks": "Vancouver" ,
                 "Buffalo Sabres":"Buffalo", "Detroit Red Wings":"Detroit",
                 "Florida Panthers":"Florida","Montreal Canadiens": "Montreal",
                "Ottawa Senators" : "Ottawa","Tampa Bay Lightning" : "TampaBay",
                 "Toronto Maple Leafs": "Toronto",  "Carolina Hurricanes":"Carolina",
                "Columbus Blue Jackets" : "Columbus ", "New Jersey Devils":"NewJersey",
                "New York Islanders" : "NYIslanders ","New York Rangers": "NYRangers",
                 "Philadelphia Flyers": "Philadelphia","Pittsburgh Penguins" : "Pittsburgh",
                 "Washington Capitals": "Washington","Arizona Coyotes" :"Arizona",
                 "Chicago Blackhawks": "Chicago", "Colorado Avalanche": "Colorado",
                 "Dallas Stars": "Dallas","Minnesota Wild" : "Minnesota",
                 "Nashville Predators": "Nashville", "St. Louis Blues" :"St.Louis",
                 "Winnipeg Jets" : "Winnipeg","Anaheim Ducks": "Anaheim" ,
                 "Calgary Flames": "Calgary" , "Edmonton Oilers": "Edmonton" ,
                 "Los Angeles Kings	": "LosAngeles", "San Jose Sharks": "SanJose" , "Vegas Golden Knights": "Vegas"
                 }
        
    url_1 = "https://www.sportsbookreviewsonline.com/scoresoddsarchives/nhl/nhl%20odds%202022-23.xlsx"
    url_2 = "https://www.sportsbookreviewsonline.com/scoresoddsarchives/nhl/nhl%20odds%202021-22.xlsx"
    r_1 = requests.get(url_1)
    r_2 = requests.get(url_2)
    with open("current_season.xlsx", "wb") as f:
        f.write(r_1.content)
    with open("last_season.xlsx", "wb") as f:
        f.write(r_2.content)
     
    current_season_xlsx = pd.read_excel("current_season.xlsx", index_col = 0)
    current_season = current_season_xlsx.to_csv("current_season.csv", encoding = "utf-8")
    last_season_xlsx = pd.read_excel("last_season.xlsx", index_col = 0)
    last_season = last_season_xlsx.to_csv("last_season.csv", encoding = "utf-8")
    #print(last_season)
    # import csv data
    current_season = pd.read_csv("current_season.csv")
    last_season = pd.read_csv("last_season.csv")
    current = current_season.iloc[::-1].reset_index().drop(["index"], axis = 1, inplace = False)
    last = last_season.iloc[::-1].reset_index().drop(["index"], axis = 1, inplace = False)
    merged = pd.concat([current, last], ignore_index = True)
    #print(merged)
    
    for i in range(len(merged["Team"].values)):
        if " " in merged["Team"].values[i]:
            teams_name = merged.iat[i, 3].replace(" ","")
            merged.loc[i, "Team"] = teams_name


    while True:
        select = input("\n \t Which data you'd like to obtain:\n\
                        a. Today's betting odds(total)\n\
                        b. Today's betting odds(team)\n\
                        c. Team's Recent Games\n\
                        d. Match Records for Two Teams\n\
                        e. Exit\n\
                        Your Choose: ")
        if select == "a":
            print(dataframe)
            choose = input("\n \tAnother Option(Y/N): ")
            if choose == "Y":
                continue
            else:
                break
        elif select == "b":
            name = input("\n \t Please Enter the Team(City Only_e.g. LosAngeles): ")
            if name not in team_dict:
                print("\n \t Wrong Name! Check Your Spelling & Spacing")
                change = input("\n \t Try Again(Y/N): ")
                if change == "Y":
                    continue
                else:
                    break
            else:
                full_name = team_dict[name]
            if full_name not in dataframe["Team"].values:
                print("\n \t No Current and Upcoming Game")
                change = input("\n \t Try Again(Y/N): ")
                if change == "Y":
                    continue
                else:
                    break
            else:
                your_team = "\nYour Team is: " + full_name
                row_index = list(dataframe["Team"].values).index(full_name)
                if row_index % 2 == 0:
                    oppo_index = row_index + 1
                else:
                    oppo_index = row_index - 1
                oppo = "You Play with: " + dataframe.iat[oppo_index, 0]
                print(your_team + "\t" + oppo + "\n")
                print(dataframe.loc[row_index])
                change = input("\n \t Return to Main Menu(R)/More Data(M)/Exit(E): ")
                if change == "R":
                    continue
                elif change == "M":
                    option = input("\n \t What do you want to further check:\n\
                        a. Your Team's Recent Records\n\
                        b. Your Team and Your Opponent Recent Records\n\
                        Your Choose: ")
                    if option == "a":
                        num_games = input("\n \t How many recent games records within this and the last season you want to see(int): ")
                        try:
                            num_games = int(num_games)
                            game_info, num, win_rate, records = get_recent_data(merged, region_dict[full_name], num_games)
                            print(f"\n \t The winning rate of {full_name} for the last {num} games is: {np.round(win_rate,2) * 100}%")
                            graph = input("\n \t See Detailed Points Plots(Y/N):")
                            if graph == "Y":
                                plot_1(game_info, num, records, num_games, team_dict, name)
                        except ValueError:
                            print("\n \t INVALID INPUT, PLEASE INPUT INTEGER")
                            continue
                    elif option == "b":
                        opponent = dataframe.iat[oppo_index, 0]
                        win, stat = get_opponent_data(merged, region_dict[full_name], region_dict[opponent])
                        print(f"\n \t Since last season, {full_name} and {opponent} have played {len(stat[0])} together\n\
                                {full_name} wins {np.round(win, 2) * 100} % of those games")
                        graph = input("\n \t See Detailed Points Plots(Y/N):")
                        if graph == "Y":
                            index = np.arange(len(stat[0])) + 1
                            compare = pd.DataFrame(stat[:2, :].T, index = index, columns = [f"{full_name}", f"{opponent}"])
                            compare.plot(kind = "bar", ylim = [0, np.max(stat[3]) + 5], rot = 0)
                            plt.title(f"{full_name} VS {opponent} since Last Season")
                            plt.plot(index - 1, stat[3], label = "Total Point")
                            plt.xlabel("Game Played")
                            plt.ylabel("Points")
                            plt.legend(loc = 1)
                            plt.show()
                        else: 
                            change = input("\n \t Return to Main Menu(R)/Exit(E): ")
                            if change == "R":
                                continue
                            else:
                                break
                    else:
                        break
                else:
                    break
        elif select == "c":
            name = input("\n \t Please Enter the Team(City Only_e.g. LosAngeles): ")
            if name not in team_dict:
                print("\n \t Wrong Name! Check Your Spelling & Spacing")
                change = input("\n \t Try Again(Y/N): ")
                if change == "Y":
                    continue
                else:
                    break
            else:
                full_name = region_dict[team_dict[name]]
                num_games = input("\n \t How many recent games records within this and the last season you want to see(int): ")
                try:
                    num_games = int(num_games)
                    game_info, num, win_rate, records = get_recent_data(merged, full_name, num_games)
                    print(f"\n \t The winning rate of {team_dict[name]} for the last {num} games is: {np.round(win_rate, 2) * 100}%")
                    graph = input("\n \t See Detailed Points Plots(Y/N):")
                    if graph == "Y":
                        plot_1(game_info, num, records, num_games, team_dict, name)
                    else: 
                        change = input("\n \t Return to Main Menu(R)/Exit(E): ")
                        if change == "R":
                            continue
                        else:
                            break
                except ValueError:
                    print("\n \t INVALID INPUT, PLEASE INPUT INTEGER")
                    continue
        elif select == "d":
            team_1 = input("\n \t Please Enter the First Team(City Only_e.g. LosAngeles): ")
            team_2 = input("\n \t Please Enter the Second Team(City Only_e.g. LosAngeles): ")
            if team_1 not in team_dict or team_2 not in team_dict:
                print("\n \t Wrong Name! Check Your Spelling & Spacing for Either Team")
                change = input("\n \t Try Again(Y/N): ")
                if change == "Y":
                    continue
                else:
                    break
            else:
                win, stat = get_opponent_data(merged, region_dict[team_dict[team_1]], region_dict[team_dict[team_2]])
                print(f"\n \t Since last season, {team_dict[team_1]} and {team_dict[team_2]} have played {len(stat[0])} games together\n\
                        {team_dict[team_1]} wins {np.round(win, 2) * 100} % of those games")
                graph = input("\n \t See Detailed Points Plots(Y/N):")
                if graph == "Y":
                    index = np.arange(len(stat[0])) + 1
                    compare = pd.DataFrame(stat[:2, :].T, index = index, columns = [f"{team_dict[team_1]}", f"{team_dict[team_2]}"])
                    compare.plot(kind = "bar", ylim = [0, np.max(stat[3]) + 5], rot = 0)
                    plt.title(f"{team_dict[team_1]} VS {team_dict[team_2]} since Last Season")
                    plt.plot(index - 1, stat[3], label = "Total Point")
                    plt.xlabel("Game Played")
                    plt.ylabel("Points")
                    plt.legend(loc = 1)
                    plt.show()
                else: 
                    change = input("\n \t Return to Main Menu(R)/Exit(E): ")
                    if change == "R":
                        continue
                    else:
                        break
        elif select == "e":
            break
        else:
            print("\n \t NO THIS OPTION,MAKE CHANGES")
            continue
    

if __name__ == "__main__":
    main()
    
    
