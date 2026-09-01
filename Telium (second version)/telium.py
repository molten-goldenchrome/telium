import time; import sys; import random

module = 1
lastModule = 0
possibleMoves = []
alive = True
won = False
power = 100
fuel = 500
locked = 0
queen = 0
ventShafts = []
infoPanels = []
workers = []

class Module():
    pass

class Player():
    pass

class Telium():
    pass

class InfoPanel():
    pass

class Worker():
    pass

class Scanner():
    pass

class Vent():
    pass

class Station():
    def __init__(self,map):
        #loads the nuumber of modules, the map
        global numModules, gameMap
        count = 1
        done = False
        while done == False:
            try:
                temp = open(f"resources/{map}/module{count}",mode="r")
                count += 1
                temp.close()
            except FileNotFoundError:
                done = True
        numModules = count
        gameMapTemp = open(f"resources/{map}/map.txt","r")
        gameMap = gameMapTemp.read()
        gameMapTemp.close()

    def getModuleInfo(module,map):
        #retrieves information about a specific module
        moves = []
        temp = open(f"resources/{map}/module{module}.txt","r")
        