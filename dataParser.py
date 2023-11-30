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

""" an obnoxiously long list of variables
that i used to have in an always-evaluates-to-true 
if stmnt for folding purposes. i miss it. """
outcome     = "outcome"         
snow        = "Snow"            #   
rain        = "RainDance"       #
sunny       = "SunnyDay"        #
sand        = "Sandstorm"     
grass       = "Grassy Terrain"  # 
mist        = "Misty Terrain"   
electric    = "Electric Terrain"
psychic     = "Psychic Terrain" 
stealthrock = "Stealth Rock"    #
spikes      = "Spikes"          #
toxicspikes = "Toxic Spikes"    #
stickyweb   = "Sticky Web"      
reflect     = "Reflect"         
lightscreen = "Light Screen"    
aurora      = "Aurora Veil"    
headers = {
    'outcome':outcome,
    'snow':snow, 
    'rain':rain, 
    'sunny':sunny, 
    'sand':sand, 
    'grass':grass, 
    'mist':mist, 
    'electric':electric, 
    'psychic':psychic,    
    'stealthrock':stealthrock, 
    'spikes':spikes, 
    'toxicspikes':toxicspikes, 
    'stickyweb':stickyweb, 
    'reflect':reflect, 
    'lightscreen':lightscreen, 
    'aurora':aurora
}
classlabels = {
    "weather": [snow, rain, sunny, sand],
    "terrain": [grass, mist, electric, psychic],
    "hazards": [stealthrock, spikes, toxicspikes, 
                stickyweb, reflect, lightscreen, aurora]
}

""" player 1 and player 2 """
p1 = 1
p2 = 2

""" a bunch of functions that could have been coded a hell of a lot better """
def get_player(line): return line.split("|")[3]

def get_weather(line):
    for weather in classlabels["weather"]:
        if weather in line:
            if p1a in line:   return weather, p1
            elif p2a in line: return weather, p2
    return None, None

def get_terrain(line):
    for terrain in classlabels["terrain"]:
        if terrain in line:
            if p1a in line:   return terrain, p1
            elif p2a in line: return terrain, p2
    return None, None

def get_hazard(line):
    for hazard in classlabels["hazards"]:
        if hazard in line:
            if p1a in line:   return hazard, p1
            elif p2a in line: return hazard, p2
    return None, None

def get_outcome(line, p1a, p2a):
    if p1a in line:   return p1   # 1
    elif p2a in line: return p2   # 2
    return None

def who_played(player):
    if player == p1a:   return p1
    elif player == p2a: return p2
    return None


""" set test to true to print strings with useful information
where applicable to be certain this works correctly
the joke is no, of course it doesn't. anyway... """
test = False


""" set folder path and output file path, 
    then open the output file for writing """
dirp = "G:/Shared drives/final learning machine/logs/"
if test: out = "astringtest.txt"
else: out = "aout.txt"


outfile = os.path.join(dirp, out)
outputfile = open(outfile, "w")


""" write the headers to the output file """
if test: outputfile.write(str(datetime.datetime.now()) + '  ||  total files (' + str(len(os.listdir(dirp))) + ') in <<' + dirp + '>>' + '\n')
for key, value in headers.items():
    outputfile.write(f"{key},")
outputfile.write("\n")


for filename in os.listdir(dirp):
    """ ignore any "a----" files, 
        they're generated by lil ol me """
    if filename.endswith(".txt") or filename.endswith(".log") and not filename.startswith("a"):
        file_path = os.path.join(dirp, filename)

        with open(file_path, 'r', encoding = 'utf8') as file:
            """ set all the variables to false or none 
            i'm getting duplicate data so this is another hacky fix """
            has_weather   = False
            weather       = None
            playedweather = None

            has_terrain   = False
            terrain       = None
            playedterrain = None

            has_hazard    = False
            hazard        = None
            playedhazard  = None

            is_game_over  = False
            p1a = None
            p2a = None
            
            for line in file:
                if '|player|p1|' in line:
                    p1a = get_player(line)
                elif '|player|p2|' in line:
                    p2a = get_player(line)

                elif '|-weather|' in line:
                    if not has_weather:
                        has_weather = True
                        weather, playedweather = get_weather(line)

                elif '|-sidestart|' in line:
                    if not has_hazard:
                        has_hazard = True
                        hazard, playedhazard = get_hazard(line)

                elif '|-fieldstart|' in line:
                    if not has_terrain:
                        has_terrain = True
                        terrain, playedterrain = get_terrain(line)

                elif '|win|' in line:
                    if not is_game_over:
                        is_game_over = True
                        outcome = get_outcome(line, p1a, p2a)

                """ k we are done with the file, 
                    now let's write to the output file
                    but respect the order of the headers 
                    this is where it gets really ugly """
                if is_game_over:
                    """ if theres no useful data, dont bother writing """
                    if has_weather or has_terrain or has_hazard:
                        
                        data = []
                        data.append(outcome)

                        if has_weather:
                            for label in classlabels["weather"]:
                                if label == weather:
                                    if test: data.append(f"{weather}<{playedweather}>")
                                    else: data.append(playedweather)
                                else: data.append("0")
                        else: 
                            if test: data.append(",,|NO WEATHER|,,")
                            else:
                                for i in range(len(classlabels["weather"])): data.append("0")


                        if has_terrain:
                            for label in classlabels['terrain']:
                                if label == terrain:
                                    if test: data.append(f"{terrain}<{playedterrain}>")
                                    else: data.append(playedterrain)
                                else: data.append("0")
                        else: 
                            if test: data.append(",,|NO TERRAIN|,,")
                            else: 
                                for i in range(len(classlabels['terrain'])): data.append("0")


                        if has_hazard:
                            for label in classlabels["hazards"]:
                                if label == hazard:
                                    if test: data.append(f"{hazard}<{playedhazard}>")
                                    else: data.append(playedhazard)
                                else: data.append("0")
                        else:
                            if test: data.append(",,,|NO HAZARDS|,,,,")
                            else:
                                for i in range(len(classlabels["hazards"])): data.append("0")

                        # print(data)
                        for item in data:
                            outputfile.write(f'{item},')
                        if test: outputfile.write(f'    >>>>  {p1a} v {p2a}')
                        outputfile.write("\n")
                    
                    else:
                        if test: outputfile.write("__NO_FUTURE__no useful data in this file ~smile~\n")
                
                    


























outputfile.write("\n\n\n>>>> let em kno that highd was here >>>>")
outputfile.close()
