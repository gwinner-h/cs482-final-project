"""
@author:    Heidi Gwinner
@date:      2023-11-06
@desc:      This is a script that takes a folder of pokemon showdown logs
            and parses them into a csv file that can be used to train a model
            to predict the outcome of a pokemon battle based on the weather,
            terrain, and hazards that are present.
"""
import os
import datetime


# set folder path, output file name, and concatenate the output file path
dirp = 'G:/Shared drives/final learning machine/testOutput' # "G:/Shared drives/final learning machine/logs/"
out = 'atest.txt'    # "aout.txt"
outfile = os.path.join(dirp, out)


# global variables
snow        = "Snow"
rain        = "RainDance"
sunny       = "SunnyDay"
sand        = "Sandstorm"
grass       = "Grassy Terrain"
mist        = "Misty Terrain"
electric    = "Electric Terrain"
psychic     = "Psychic Terrain"
trickroom   = "Trick Room"
stealthrock = "Stealth Rock"
toxicspikes = "Toxic Spikes"
spikes      = "Spikes"
stickyweb   = "Sticky Web"
reflect     = "Reflect"
lightscreen = "Light Screen"
aurora      = "Aurora Veil"
tailwind    = "Tailwind"
outcome     = "outcome"
headers = {
    'snow1':snow,
    'snow2':snow,
    'rain1':rain,
    'rain2':rain,
    'sunny1':sunny,
    'sunny2':sunny,
    'sand1':sand,
    'sand2':sand,
    'grass1':grass,
    'grass2':grass,
    'mist1':mist,
    'mist2':mist,
    'electric1':electric,
    'electric2':electric,
    'psychic1':psychic,
    'psychic2':psychic,
    'trickroom1':trickroom,
    'trickroom2':trickroom,
    'stealthrock1':stealthrock,
    'stealthrock2':stealthrock,
    'toxicspikes1':toxicspikes,
    'toxicspikes2':toxicspikes,
    'spikes1':spikes,
    'spikes2':spikes,
    'stickyweb1':stickyweb,
    'stickyweb2':stickyweb,
    'reflect1':reflect,
    'reflect2':reflect,
    'lightscreen1':lightscreen,
    'lightscreen2':lightscreen,
    'aurora1':aurora,
    'aurora2':aurora,
    'tailwind1':tailwind,
    'tailwind2':tailwind,
    'outcome':outcome
}
classlabels = {
    "weather": [snow, rain, sunny, sand],
    "terrain": [grass, mist, electric, psychic, trickroom],
    "hazards": [stealthrock, toxicspikes, spikes, stickyweb],
    "screens": [reflect, lightscreen, aurora, tailwind],
}
snow1      = "Snow1"
snow2      = "Snow2"
rain1      = "Rain1"
rain2      = "Rain2"
sunny1     = "Sunny1"
sunny2     = "Sunny2"
sand1      = "Sand1"
sand2      = "Sand2"
grass1     = "Grass1"
grass2     = "Grass2"
mist1      = "Mist1"
mist2      = "Mist2"
electric1  = "Electric1"
electric2  = "Electric2"
psychic1   = "Psychic1"
psychic2   = "Psychic2"
trickroom1 = "Trickroom1"
trickroom2 = "Trickroom2"
stealthrock1 = "Stealthrock1"
stealthrock2 = "Stealthrock2"
toxicspikes1 = "Toxicspikes1"
toxicspikes2 = "Toxicspikes2"
spikes1      = "Spikes1"
spikes2      = "Spikes2"
stickyweb1   = "Stickyweb1"
stickyweb2   = "Stickyweb2"
reflect1     = "Reflect1"
reflect2     = "Reflect2"
lightscreen1 = "Lightscreen1"
lightscreen2 = "Lightscreen2"
aurora1      = "Aurora1"
aurora2      = "Aurora2"
tailwind1    = "Tailwind1"
tailwind2    = "Tailwind2"
playerlabels = {
    "player_weather": [snow1, snow2, sunny1, sunny2, rain1, rain2, sand1, sand2],
    "player_terrain": [grass1, grass2, mist1, mist2, electric1, electric2, 
                       psychic1, psychic2, trickroom1, trickroom2],
    "player_hazards": [stealthrock1, stealthrock2, toxicspikes1, toxicspikes2,
                       spikes1, spikes2, stickyweb1, stickyweb2],
    "player_screens": [reflect1, reflect2, lightscreen1, lightscreen2, 
                       aurora1, aurora2, tailwind1, tailwind2],
}

# this sets the player names to None
p1_name = None
p2_name = None
p1_moves = []
p2_moves = []

is_game_over  = False

spike1_counter = 0
toxic1_counter = 0
spike2_counter = 0
toxic2_counter = 0

# player 1 and player 2 return values
player1 = 1
player2 = 2 # i changed this from 1 to 2...since player1 is also set to 1, lol
p1      = 'p1'
p2      = 'p2'
p1a     = 'p1a'
p2a     = 'p2a'

# literal strings for checking line
p1_line      = '|player|p1|'
p2_line      = '|player|p2|'
weather_line = '|-weather|'
terrain_line = '|-fieldstart|'
hazard_line  = '|-sidestart|'
win_line     = '|win|'


""" function definitions """
# writes headers
def print_headers():
    for key, value in headers.items():
        outputfile.write(f"{key},")
    outputfile.write('\n')
    return None

# resets all the variables to false or none
def reset_vars():
    global p1_name, p2_name, is_game_over
    global spike1_counter, toxic1_counter, spike2_counter, toxic2_counter

    is_game_over  = False
    p1_name = None   # holds player1 username
    p2_name = None   # holds player2 username
    spike1_counter = 0
    toxic1_counter = 0
    spike2_counter = 0
    toxic2_counter = 0

    return None

# clears the arrays
def clear_arrays():
    global p1_moves, p2_moves

    p1_moves.clear()
    p2_moves.clear()
    return None

# function that returns the player name
def set_player(line): 
    return line.split("|")[3]

# returns the player that played the move
def get_player(player):
    if player == p1_name or player == p1a:
        return player1  # returns 1
    elif player == p2_name or player == p2a:
        return player2  # returns 2
    return None

# returns the weather and the player that played it
def get_weather(line):
    for weather in classlabels["weather"]:
        if weather in line:
            if p1a in line:
                return weather, player1
            elif p2a in line:
                return weather, player2
    return None, None

# returns the terrain and the player that played it
def get_terrain(line):
    for terrain in classlabels["terrain"]:
        if terrain in line:
            if p1a in line:
                return terrain, player2
            elif p2a in line:
                return terrain, player1
    return None, None

# returns the hazard and the player that played it, hazards and screens are in the same |- line, so must check for both
def get_hazard(line):
    # check if the line contains a hazard
    for hazard in classlabels["hazards"]:
        if hazard in line:
            if hazard == spikes or hazard == toxicspikes:
                if p1_name in line:                     # if p1 is in |-sidestart| line, then p2 played the hazard
                    update_counter(hazard, player2)     # update the counter for player2
                elif p2_name in line:
                    update_counter(hazard, player1)     # update the counter for player1

            if p2_name in line:                         # player1 played hazard
                return hazard, player1
            elif p1_name in line:                       # player2 played hazard
                return hazard, player2
    
    # if the line does not contain a hazard, check for screens
    for screen in classlabels["screens"]:
        if screen in line:
            if p1_name in line:
                return screen, player1
            elif p2_name in line:
                return screen, player2
    return None, None

# updates the appropriate counter for the spike and/or toxic spike hazard
def update_counter(hazard, player):
    global spike1_counter, toxic1_counter, spike2_counter, toxic2_counter

    if player == player1:
        if hazard == toxicspikes:
            if toxic1_counter < 2:
                toxic1_counter += 1
        elif hazard == spikes:
            if spike1_counter < 3:
                spike1_counter += 1
            
    elif player == player2:
        if hazard == toxicspikes:
            if toxic2_counter < 2:
                toxic2_counter += 1
        elif hazard == spikes:
            if spike2_counter < 3:
                spike2_counter += 1
    return None

# checks if the weather is already in the player array
def check_weather(weather, player_moves):
    for played_weather in player_moves:
        if weather == played_weather:
            return True
    return False

# checks if the terrain is already in the player array
def check_terrain(terrain, player_moves):
    for played_terrain in player_moves:
        if terrain == played_terrain:
            return True
    return False

# checks if the hazard is already in the player array
def check_hazard(hazard, player_moves):
    for played_moves in player_moves:
        if hazard == played_moves:
            return True
    return False

# returns the outcome/winner of the battle
def get_outcome(line, p1a, p2a):
    if p1a in line:   
        return '0'  # player1 won
    elif p2a in line: 
        return '1'  # player2 won
    return None

# sets the output to be printed to the output file
def set_output():
    global p1_moves, p2_moves, spike1_counter, toxic1_counter, spike2_counter, toxic2_counter

    # holds the data that will be written to the output file
    data = []

    # iterate over player labels, check if each condition was played by the players
    for label in classlabels.keys():
        for condition in classlabels[label]:

            # check if the condition was played by player1
            if condition in p1_moves:
                if condition == spikes:
                    data.append(spike1_counter)
                elif condition == toxicspikes:
                    data.append(toxic1_counter)
                else:
                    data.append('1')
            else:   # condition was not played by player1
                data.append('0')
            # check if the condition was played by player2
            if condition in p2_moves:
                if condition == spikes:
                    data.append(spike2_counter)
                elif condition == toxicspikes:
                    data.append(toxic2_counter)
                else:
                    data.append('1')
            else:   # condition was not played by player2
                data.append('0')
    return data

# writes the data to the output file
def print_data(data):
    for item in data:
        outputfile.write(f'{item},')
    outputfile.write('\n')
    return None



""" main """
# open the output file & write the headers to the file
outputfile = open(outfile, "w")
print_headers()

# traverse the folder that contains the logs
for filename in os.listdir(dirp):
    # ignores any "a----" files, they're generated by lil ol me
    if filename.endswith(".txt") or filename.endswith(".log") and not filename.startswith("a"):
        
        # set the file path & open the file
        file_path = os.path.join(dirp, filename)
        with open(file_path, 'r', encoding = 'utf8') as file:         
            # reset the variables and clear the arrays
            reset_vars()
            clear_arrays()

            # iterate over each line in the file
            for line in file:
                # set the player names
                if p1_line in line:
                    p1_name = set_player(line)
                elif p2_line in line:
                    p2_name = set_player(line)

                # if the line contains weather, get the weather and who played it
                elif weather_line in line:
                    weather, who_played_weather = get_weather(line)
                    if who_played_weather == player1:
                        if check_weather(weather, p1_moves):
                            continue
                        else:
                            p1_moves.append(weather)
                    elif who_played_weather == player2:
                        if check_weather(weather, p2_moves):
                            continue
                        else:
                            p2_moves.append(weather)

                # hazards and screens show up in the same line
                elif hazard_line in line:
                    hazard, who_played_hazard = get_hazard(line)

                    # if the hazard has been played by the player before, do not append
                    if who_played_hazard == player1:
                        if check_hazard(hazard, p1_moves):
                            continue
                        else:
                            p1_moves.append(hazard)
                    elif who_played_hazard == player2:
                        if check_hazard(hazard, p2_moves):
                            continue
                        else:
                            p2_moves.append(hazard)

                # if the line contains terrain, get the terrain and who played it
                elif terrain_line in line:
                    terrain, who_played_terrain = get_terrain(line)
                    if who_played_terrain == player1:
                        if check_terrain(terrain, p1_moves):
                            continue
                        else:
                            p1_moves.append(terrain)
                    elif who_played_terrain == player2:
                        if check_terrain(terrain, p2_moves):
                            continue
                        else:
                            p2_moves.append(terrain)

                # if the line contains a win, get the outcome
                elif win_line in line:
                    if not is_game_over:
                        is_game_over = True
                        outcome = get_outcome(line, p1_name, p2_name)

                # we are done with the file, now let's write to the output file but respect the order of the headers 
                if is_game_over:

                    # set the output to be printed to the output file
                    output = set_output()

                    # append the outcome to the data array
                    output.append(outcome)

                    # write the data to the output file
                    print_data(output)

                    break
outputfile.close()