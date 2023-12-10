"""
@author:    Heidi Gwinner
@date:      2023-11-06
@desc:      This is a script that takes a folder of pokemon showdown logs
            and parses them into a csv file that can be used to train a model
            to predict the outcome of a pokemon battle based on the weather,
            terrain, and hazards that are present.

i think this is entirely just a nasty hackjob
200 lines if nested if statements and for loops 
"""
import os
import datetime


# set folder path, output file name, and concatenate the output file path
dirp = "G:/Shared drives/final learning machine/logs/"
out = "aout.txt"
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
spikes      = "Spikes"
toxicspikes = "Toxic Spikes"
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
    'spikes1':spikes,
    'spikes2':spikes,
    'toxicspikes1':toxicspikes,
    'toxicspikes2':toxicspikes,
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
    "hazards": [stealthrock, spikes, toxicspikes, stickyweb],
    "screens": [reflect, lightscreen, aurora, tailwind],
}

# this sets the player names to None
p1_name = None
p2_name = None
is_game_over  = False

has_weather    = False
p1_has_weather = False
p2_has_weather = False
weather        = None
playedweather  = None

has_terrain    = False
p1_has_terrain = False
p2_has_terrain = False
terrain        = None
playedterrain  = None

has_hazard    = False
p1_has_hazard = False
p2_has_hazard = False
hazard        = None
playedhazard  = None

has_screen    = False
p1_has_screen = False
p2_has_screen = False
screen        = None
playedscreen  = None

spike1_counter = 0
toxic1_counter = 0
spike2_counter = 0
toxic2_counter = 0

# player 1 and player 2 return values
player1 = 1
p1 = 'p1'
p1a = 'p1a'
player2 = 2
p2 = 'p2'
p2a = 'p2a'

# literal strings for checking line
p1_line = '|player|p1|'
p2_line = '|player|p2|'
weather_line = '|-weather|'
terrain_line = '|-fieldstart|'
hazard_line = '|-sidestart|'
win_line = '|win|'


""" function definitions """
# writes headers
def print_headers():
    if stringTest: 
        outputfile.write(str(datetime.datetime.now()) + '  ||  total files (' + 
                         str(len(os.listdir(dirp))) + ') in <<' + dirp + '>>' + '\n\n')
    
    for key, value in headers.items():
        outputfile.write(f"{key},")
    outputfile.write('\n')

# resets all the variables to false or none
def reset_vars():
    global is_game_over, p1_name, p2_name
    global has_weather, weather, playedweather
    global p1_has_weather, p2_has_weather
    global has_terrain, terrain, playedterrain
    global p1_has_terrain, p2_has_terrain
    global has_hazard, hazard, playedhazard
    global p1_has_hazard, p2_has_hazard
    global has_screen, screen, playedscreen
    global p1_has_screen, p2_has_screen
    global spike1_counter, toxic1_counter, spike2_counter, toxic2_counter

    is_game_over  = False
    p1_name = None   # holds player1 username
    p2_name = None   # holds player2 username

    has_weather   = False
    p1_has_weather = False
    p2_has_weather = False
    weather       = None
    playedweather = None

    has_terrain   = False
    p1_has_terrain = False
    p2_has_terrain = False
    terrain       = None
    playedterrain = None

    has_hazard    = False
    p1_has_hazard = False
    p2_has_hazard = False
    hazard        = None
    playedhazard  = None

    spike1_counter = 0
    toxic1_counter = 0
    spike2_counter = 0
    toxic2_counter = 0

    has_screen   = False
    p1_has_screen = False
    p2_has_screen = False
    screen       = None
    playedscreen = None

    return None

# function that returns the player name
def set_player(line): 
    return line.split("|")[3]

# returns the player that played the move
def who_played(player):
    if player == p1_name or player == p1a:
        return player1  # returns 1
    elif player == p2_name or player == p2a:
        return player2  # returns 2
    return None

# returns the weather and the player that played it
def get_weather(line):
    global has_weather, p1_has_weather, p2_has_weather

    for weather in classlabels["weather"]:
        if weather in line:
            has_weather = True

            if p1a in line:
                p1_has_weather = True
                return weather, player1
            elif p2a in line:
                p2_has_weather = True
                return weather, player2
            
    return None, None

# returns the terrain and the player that played it
def get_terrain(line):
    global has_terrain, p1_has_terrain, p2_has_terrain

    for terrain in classlabels["terrain"]:
        if terrain in line:
            has_terrain = True

            if p1a in line:
                p1_has_terrain = True
                return terrain, player2
            elif p2a in line:
                p2_has_terrain = True
                return terrain, player1
            
    return None, None

# returns the hazard and the player that played it, hazards and screens are in the same |- line, so must check for both
def get_hazard(line):
    """ for hazard in classlabels['hazards']:
            # if p1_name in line:   
            #     return hazard, player2
            # elif p2_name in line: 
            #     return hazard, player1 """
    global has_hazard, p1_has_hazard, p2_has_hazard

    for hazard in (classlabels["hazards"]) or screen in classlabels["screens"]:
        # p1a uses hazard (prev line: |move|p1a:), but p2 is affected by it (|-sidestart|p1: )
        if hazard in line:
            has_hazard = True

            # if p1 is in sidestart line, then p2 played the hazard
            if hazard == spikes or hazard == toxicspikes:
                if p1_name in line:
                    match(hazard, player2)  # update the counter for player2
                if p2_name in line:
                    match(hazard, player1)  # update the counter for player1

            # not spikes or toxicspikes
            if p2_name in line:
                p1_has_hazard = True
                return hazard, player1
            elif p1_name in line:
                p2_has_hazard = True
                return hazard, player2
            
        elif screen in line:
            return get_screens(line)
    return None, None

# updates the appropriate counter for the hazard
def match(hazard, player):
    global spike1_counter, toxic1_counter, spike2_counter, toxic2_counter

    if hazard == spikes and player == player1:
        spike1_counter += 1
    elif hazard == toxicspikes and player == player1:
        toxic1_counter += 1
    elif hazard == spikes and player == player2:
        spike2_counter += 1
    elif hazard == toxicspikes and player == player2:
        toxic2_counter += 1

    """ if hazard == spikes: 
    #     spike_counter += 1
    # elif hazard == toxicspikes: 
    #     toxic_counter += 1 """
    return None

# returns the screen and the player that played it
def get_screens(line):
    global has_screen, p1_has_screen, p2_has_screen

    # p1a uses screen (prev line: |move|p1a:) and is affected by it (|-sidestart|p1: )
    for screen in classlabels["screens"]:
        if screen in line:
            has_screen = True

            if p1_name in line:
                p1_has_screen = True
                return screen, player1
            elif p2_name in line:
                p2_has_screen = True
                return screen, player2
    return None, None

# returns the outcome/winner of the battle
def get_outcome(line, p1a, p2a):
    if p1a in line:   
        return '0'  # 1
    elif p2a in line: 
        return '1'  # 2
    return None


""" main """
# open the output file & write the headers to the file
outputfile = open(outfile, "w")
print_headers()

# traverse the folder that contains the logs
for filename in os.listdir(dirp):

    # ignores any "a----" files, they're generated by lil ol me
    if filename.endswith(".txt") or filename.endswith(".log") and not filename.startswith("a"):
        
        # set the file path
        file_path = os.path.join(dirp, filename)

        # open the file
        with open(file_path, 'r', encoding = 'utf8') as file:

            # set all the variables to false or none
            reset_vars()
            
            # iterate over each line in the file
            for line in file:

                # set the player names
                if p1_line in line:
                    p1_name = set_player(line)
                elif p2_line in line:
                    p2_name = set_player(line)

                elif weather_line in line:
                    weather, playedweather = get_weather(line)

                # hazards and screens show up in the same line
                elif hazard_line in line:
                    hazard, playedhazard = get_hazard(line)

                elif terrain_line in line:
                    terrain, playedterrain = get_terrain(line)

                elif win_line in line:
                    if not is_game_over:
                        is_game_over = True
                        outcome = get_outcome(line, p1_name, p2_name)

                """ TODO: FIX ALL OF THE OUTPUT! DOES NOT EVALUATE CORRECTLY WHO PLAYED WHAT FOR ALL EFFECTS """
                # we are done with the file, now let's write to the output file but respect the order of the headers 
                if is_game_over:

                    # holds the data that will be written to the output file
                    data = []

                    # TODO: fix evaluating who played weather
                    if has_weather:
                        for label in classlabels["weather"]:
                            if label == weather:
                                data.append(playedweather)
                            else: 
                                data.append('0')
                    else: 
                        for i in range(len(classlabels['weather'])): 
                            data.append("0")

                    # TODO: fix evaluating who played terrain
                    if has_terrain:
                        for label in classlabels['terrain']:
                            if label == terrain:
                                data.append(playedterrain)
                            else: 
                                data.append('0')
                    else: 
                        if stringTest: 
                            data.append('|x,x,x,x,x|')
                        else: 
                            for i in range(len(classlabels['terrain'])): 
                                data.append('0')


                    # TODO: fix evaluating who played hazard and what hazard was played
                    if has_hazard:
                        for label in classlabels["hazards"]:
                            if label == hazard:
                                if playedhazard == p1_name:
                                    if hazard == spikes:
                                        data.append(spike1_counter)
                                        data.append('0')
                                    elif hazard == toxicspikes:
                                        data.append(toxic1_counter)
                                        data.append('0')
                                    else:
                                        data.append(playedhazard)
                                        data.append('0')
                                elif playedhazard == p2_name:
                                    if hazard == spikes:
                                        data.append('0')
                                        data.append(spike2_counter)
                                    elif hazard == toxicspikes:
                                        data.append('0')
                                        data.append(toxic2_counter)
                                    else:
                                        data.append('0')
                                        data.append(playedhazard)
                            else:
                                data.append('0')
                        else: # THIS PART DOES NOT WORK SINCE THERE ARE NOW TWO COLUMNS FOR EVERY HAZARD
                            for i in range(len(classlabels["hazards"])): 
                                data.append('0')
                    

                    # TODO: fix evaluating who played screen
                    if has_screen:
                        for label in classlabels["screens"]:
                            if label == screen:
                                data.append(playedscreen)
                            else: 
                                data.append('0')
                    else:
                        for i in range(len(classlabels["screens"])): 
                            data.append('0')
                    
                    # print who won, 0 = player1, 1 = player2
                    data.append(outcome)

                    # write the data to the output file
                    for item in data:
                        outputfile.write(f'{item},')
                    outputfile.write('\n')

                    break
outputfile.close()