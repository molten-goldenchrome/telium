import time; import sys; import random

class Module:
    currentModule = 1
    lastModule = 0
    def __init__(self):
        pass

    def loadModule(self):
        global module
        possibleMoves,roomInfo = station.getModuleInfo(module,station.map)
        station.outputModule(module,roomInfo); station.outputMoves(possibleMoves)

    def getCurrentModule(self):
        return self.currentModule

    def getLastModule(self):
        return self.lastModule

    def getPossibleMoves(self):
        return station.getModuleInfo(module,station.map)[0]



class Player:
    alive = True
    won = False
    def __init__(self):
        pass

    def getAction(self):
        localModule = module.getCurrentModule()
        localPossibleMoves = module.getPossibleMoves()
        validAction = False
        while validAction == False:
            print("What do you want to do next? (MOVE, SCANNER)")
            action = input(">>>")
            result,detail = textParser(action)
            if result == 'move' and detail in localPossibleMoves:
                validAction = True; module.lastModule = localModule; module.currentModule = detail
            elif result == 'move' and detail == None:
                try:
                    newModule = int(input("Which module would you like to go to?\n>"))
                    if newModule in localPossibleMoves:
                        validAction = True; module.lastModule = localModule; module.currentModule = newModule
                except TypeError:
                    print("You must type an integer with nothing around it, e.g. '6'.")
            


class Telium:
    queen = 0

class InfoPanel:
    infoPanels = []

class Worker:
    workers = []

class Scanner:
    pass

class Vent:
    ventShafts = []

class Station:
    map = "Charles_Darwin"
    power = 100
    fuel = 500
    locked = 0
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

    def getModuleInfo(self,module,map):
        #retrieves information about a specific module
        moves = []
        temp = open(f"resources/{map}/module{module}.txt","r")
        for i in range(0,4):
            moveRead = temp.readline()
            moveRead = int(moveRead.strip())
            if moveRead != 0:
                moves.append(moveRead)
        roomInfo = temp.readline()
        temp.close()
        return moves,roomInfo

    def outputModule(self,module,roomInfo):
        print(f"\n-------------------------------------------------\nYou are in module {module}.\n{roomInfo}")

    def outputMoves(self,possibleMoves):
        print(f"From here, you can move to modules: | ",end='')
        for move in possibleMoves:
            print(move,'| ',end='')
        print()

def textParser(command):
    global power, module, infoPanels
    command = command.lower()
    command = command.strip(' ')
    command = command.strip(".")
    action = None
    detail = None
    if 'move' in command or ('m' in command and 'map' not in command):
        action = 'move'
        command = command.strip("move")
        if command == '':
            return(action,None)
        try:
            detail = int(command)
            return (action,detail)
        except:
            return (False,False)
    elif 'map' in command:
        action = 'map'
        return (action,detail)
    elif 'look' in command:
        action = 'look'
        return (action,detail)
    elif 'scanner' in command:
        return ("scanner",None)
    elif 'lock' in command or ('l' in command and 'lock' not in command):
        action = 'lock'
        command = command.strip("lock")
        try:
            detail = int(command)
            return (action,detail)
        except:
            return (False,False)
    elif 'panel' in command:
        if power >= 51 and module in infoPanels:
            return ('panel',"allowed")
        else:
            return ('panel','not allowed')
    else:
        return (False,False)

def mainMenu():
    print("Welcome to Telium!")
    validAction = False
    while not validAction:
        print("1. Play\n2. Instructions\n3. Quit (1,2,3)")
        action = input(">>>")
        if action == "1":
            validAction = True
        elif action == "2":
            print("Please see 'instructions.md' in the same folder as this python file")
        elif action == "3":
            sys.exit()
        else:
            print("Not a valid option. Please enter as an integer on its own, e.g. '1' to play the game.")

module = Module()
station = Station(map="Charles_Darwin") #change this so custom ones can be made
scanner = Scanner()
vents = Vent()
workers = Worker()
player = Player()
panels = InfoPanel()
queen = Telium()

while player.alive and not player.won:
    module.loadModule()
    if player.won == False and player.alive == True:
        player.getAction()

if player.won:
    print("The queen is trapped! You burn it to death with your flamethrower.")
    print("Game over! You win!")

if not player.alive:
    print("The station has run out of power. Unable to sustain life support, you die.")
    print("Game over! You lose!")