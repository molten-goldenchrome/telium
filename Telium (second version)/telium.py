import time; import sys; import random; import threading; from threading import Event

threadDict = {}


class Module:
    currentModule = 1
    lastModule = 0
    def __init__(self):
        pass

    def loadModule(self):
        possibleMoves,roomInfo = station.getModuleInfo(self.currentModule,station.map)
        station.outputModule(self.currentModule,roomInfo); station.outputMoves(possibleMoves)
        if station.fuel <= 100:
            print("LOW FUEL!")
        if self.currentModule == queen.queen:
            print("The queen glares at you...")
            queen.moveQueen()
        else:
            if self.currentModule in workers.workerList:
                print("A worker alien glares at you...")
            elif self.currentModule in panels.infoPanels:
                print("There is an information panel in here. You could use it to scan for lifeforms.")
            elif self.currentModule in vents.ventShafts:
                print("There is a ventilation shaft in here. You feel its cool air blowing past you.")
                time.sleep(3)
                print("There is also a bank of fuel cells in here. You load a cell into your flamethrower.")
                fuelGained = random.randint(2,5)*10
                print(f"Fuel was {station.fuel}, now reading {station.fuel+fuelGained}.")
                station.fuel = station.fuel + fuelGained
                time.sleep(2)
                print("The doors suddenly lock shut!")
                time.sleep(1)
                print("What is happening to the station?!")
                time.sleep(0.5)
                print("Our only escape is to climb into the ventilation shaft.")
                time.sleep(0.25)
                print("Where do we go?!")
                time.sleep(0.25)
                print("We follow the passage and find ourselves sliding down.")
                self.lastModule = self.currentModule
                while self.currentModule in vents.ventShafts:
                    self.currentModule = random.randint(1,station.numModules)
                self.loadModule()
            queen.moveQueen()

    def lockModule(self):
        localNumModules = station.numModules
        try:
            toLock = int(input("Enter module to lock:\n>>>"))
            if toLock < 0 or toLock > localNumModules:
                print("Invlaid module - operation failed.")
            elif toLock == queen.queen:
                print("Operation failed. Unable to lock module.")
            elif toLock == station.locked:
                print("Operation failed. Module is already locked!")
            else:
                station.locked = toLock
                print(f"Aliens cannot enter module {toLock}.")
                powerUsed = 25 + 1*random.randint(0,10)
                station.power -= powerUsed
        except TypeError:
            print("Incorrectly entered module! Must be an integer on its own, e.g. '6'.")

    def lockKnownModule(self,toLock):
        localNumModules = station.numModules
        try:
            if toLock < 0 or toLock > localNumModules:
                print("Invlaid module - operation failed.")
            elif toLock == queen.queen:
                print("Operation failed. Unable to lock module.")
            else:
                station.locked = toLock
                print(f"Aliens cannot enter module {toLock}.")
                powerUsed = 25 + 1*random.randint(0,10)
                station.power -= powerUsed
        except TypeError:
            print("Incorrectly entered module! Must be an integer on its own, e.g. '6'.")


    def getCurrentModule(self):
        return self.currentModule

    def getLastModule(self):
        return self.lastModule

    def getPossibleMoves(self):
        return station.getModuleInfo(module,station.map)[0]



class Player:
    alive = True
    won = False
    hp = 100
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
            elif result == "scanner":
                validAction = True
                scanner.scannerCalled()
            elif result == "lock":
                validAction = True
                module.lockKnownModule(detail)

class Telium:
    queen = 0
    hp = 100
    def __init__(self):
        pass

    def moveQueen(self):
        localModule = module.getCurrentModule()
        localLastModule = module.getLastModule()
        localLocked = station.locked
        localQueen = self.queen
        if localModule == localQueen:
            movesToMake = random.randint(1,3)
            canMoveToLastModule = False
            while movesToMake > 0:
                escapes,ignore = station.getModuleInfo(queen.queen,station.map)
                if localModule in escapes:
                    escapes.remove(localModule)
                if localLastModule in escapes and canMoveToLastModule == False:
                    escapes.remove(localLastModule)
                if localLocked in escapes:
                    escapes.remove(localLocked)
                if len(escapes) == 0:
                    player.won = True
                    movesToMake = 0
                    print("...and the door is locked. It's trapped.")
                    self.finalBattle()
                else:
                    if movesToMake == 1:
                        print("...and has escaped.")
                    self.queen = random.choice(escapes)
                    movesToMake = movesToMake -1
                    canMoveToLastModule = True
                    while queen.queen in vents.ventShafts:
                        if movesToMake > 1:
                            print("...and has escaped.")
                        print("We can hear scuttling in the vent shafts.")
                        validMove = False
                        while not validMove:
                            queen.queen = random.randint(1,station.numModules)
                            if queen.queen not in vents.ventShafts:
                                validMove = True
                        movesToMake = 0

    def finalBattle(self):
        time.sleep(2)
        print("The queen glares at you with her sparkling, ruby eyes.")
        time.sleep(0.5)
        print("You glare back.")
        time.sleep(2)
        print("You charge up your flamethrower!")
        threadDict["QTEtracker"] = threading.Thread(target=self.quickTimeEventStarter)

    def quickTimeEventStarter(self):
        global threadDict
        while queen.hp > 0 and station.fuel > 0 and player.hp > 0:
            eventTypes = ["swipe","flamethrowerJam","debris","stunChancePlayer","stunChanceQueen"]
            event = random.choice(eventTypes)
            while not threading.active_count() == 1:
                time.sleep(random.randint(10,20))
                self.hp -= 10; station.fuel -= 10
            if event == "swipe":
                threadDict["swipe"] = threading.Thread(target=self.swipeEvent)
                threadDict["timeTracker"] = threading.Thread(target=self.quickTimeEventTracker,args=(time.time(),random.uniform(0.5,1.5)))
                threadDict["completedEvent"] = Event()
                threadDict["killEvent"] = Event()
                threadDict["swipe"].start(); threadDict["timeTracker"].start()
                threadDict["swipe"].join(); threadDict["timeTracker"].join()
                if threadDict["completedEvent"].is_set() and not threadDict["killEvent"].is_set():
                    print("Good dodge! Just in time.")
                elif threadDict["completedEvent"].is_set() and threadDict["killEvent"].is_set():
                    print("You try to jump out the way, but the queen hits you with a glancing blow.")
                else:
                    print("The queen hits you with a solid blow to the chest. That hurt!")
            elif event == "flamethrowerJam":
                threadDict["flamethrowerJam"] = threading.Thread(target=self.flamethrowerJamEvent)
                threadDict["timeTracker"] = threading.Thread(target=self.quickTimeEventTracker,args=(time.time(),random.uniform(0.5,1.5)))
                threadDict["completedEvent"] = Event()
                threadDict["killEvent"] = Event()
                threadDict["flamethrowerJam"].start(); threadDict["timeTracker"].start()
                threadDict["flamethrowerJam"].join(); threadDict["timeTracker"].join()
            elif event == 
        

    def quickTimeEventTracker(self,startTime,allowedTime):
        global threadDict
        timeMustFinish = startTime+allowedTime
        while time.time < timeMustFinish and not threadDict["completedEvent"].is_set():
            pass
        if time.time > timeMustFinish:
            threadDict["killEvent"].set()
        else:
            pass

    def swipeEvent(self):
        global threadDict
        while not threadDict["killEvent"].is_set:
            print("THE QUEEN SWIPES AT YOU! ENTER TO DODGE!")
            input()
            threadDict["completedEvent"].set()
            break

    def flamethrowerJamEvent(self):
        global threadDict
        while not threadDict["killEvent"].is_set():
            alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            strToFix = ''
            for i in range(4):
                strToFix = strToFix+random.choice(alphabet)
            print("Your flamethrower got jammed! Type",strToFix,"to repair it!")
            entered = input(">>>")
            if entered.lower() == strToFix.lower():
                threadDict["completedEvent"].set()
                break


class InfoPanel:
    infoPanels = []

class Worker:
    workerList = []

class Scanner:
    def __init__(self):
        pass

    def scannerCalled(self):
        print("SYSTEMATIC CAPTURE AND NETWORK NAVIGATION EGINE FOR RETRIEVAL (v6.1.12)")
        print("loading...")
        time.sleep(3)
        print("SCANNER READY. ENTER COMMAND: (LOCK, POWER)")
        command = input(">>>")
        if command.lower() == "lock":
            module.lockModule()
        elif command.lower() == 'power':
            print("FETCHING DATA...")
            time.sleep(1.5)
            print(f"STATION POWER READING AT {station.power}%")
        elif command.lower() == 'fuel':
            print("FETCHING DATA...")
            time.sleep(1.5)
            print(f"FUEL READING AT {station.fuel}.")
        elif command.lower() == 'lifeforms':
            print("FETCHING DATA...")
            time.sleep(1.5)
            print(f"{len(workers.workerList)+1} ALIEN LIFEFORMS DETECTED ONBOARD")
        else:
            print("UNKNOWN OR INCORRECT COMMAND. PLEASE REFER TO DOCUMENTATION.")

class Vent:
    ventShafts = []

class Station:
    map = "Charles_Darwin"
    power = 100
    fuel = 500
    locked = 0
    numModules = 0
    gameMap = ""
    def __init__(self,map):
        #loads the nuumber of modules, the map
        count = 1
        done = False
        while done == False:
            try:
                temp = open(f"resources/{map}/module{count}",mode="r")
                count += 1
                temp.close()
            except FileNotFoundError:
                done = True
        self.numModules = count
        gameMapTemp = open(f"resources/{map}/map.txt","r")
        self.gameMap = gameMapTemp.read()
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

    def spawnNPCs(self):
        localNumModules = self.numModules
        moduleSet = []
        for counter in range(2,localNumModules+1):
            moduleSet.append(counter)
        random.shuffle(moduleSet)
        i = 0
        queen.queen = moduleSet[i]
        for counter in range(0,3):
            i += 1
            vents.ventShafts.append(moduleSet[i])
        for counter in range(0,2):
            i +=1
            panels.infoPanels.append(moduleSet[i])
        for counter in range(0,3):
            i+=1
            workers.workerList.append(moduleSet[i])

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

station.spawnNPCs() 

while player.alive and not player.won:
    module.loadModule()
    if player.won == False and player.alive == True:
        player.getAction()
        station.power -= 1

if player.won:
    print("The queen is trapped! You burn it to death with your flamethrower.")
    print("Game over! You win!")

if not player.alive:
    print("The station has run out of power. Unable to sustain life support, you die.")
    print("Game over! You lose!")