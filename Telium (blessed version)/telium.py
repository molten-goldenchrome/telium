import blessed; import time; import random; import sys
term = blessed.Terminal()

num_modules = 12
module = 1
lastModule = 0
visitedModules = []
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
global roomInfo

gameMap = r"""
         [ 1 ]-------------------[ 2 ]-------------------[ 3 ]
         / | |                                           / |
        /  | \                   +-----------------------+ |
       /   |  \                  |                         |
      /    |   `---+             |                         |
   [ 8 ]   |     [ 9 ]---------[ 12 ]                    [ 4 ]
     |     |      /             /                          |
     |     |     /             /                           |
     |     |    /             /                            |
     |     |   /             /                             |
     |   [ 10 ]             /                              |
     |     |               /                               |
     |     |              /                                |
     |     |             /                                 |
     |     \            /                                  |
     |      `--------[ 11 ]                      +-------[ 5 ]
     |                  |                       /        /
      \                 +----------------------+        / 
       \                                                /  
        \                                              /   
         `-------[ 7 ]-------------------------------[ 6 ]
"""

def loadModule():
    """Loads the current module for other functions."""
    global module, possibleMoves
    possibleMoves = getModulesFrom(module)
    outputModule()
    checkVents()
    move_queen()

def getModulesFrom(module):
    global roomInfo
    """Finds possible moves from the current module."""
    moves = []
    textHandle = open("resources/Charles_Darwin/module" + str(module) + ".txt","r")
    for i in range(5):
        moveRead = textHandle.readline()
        if i != 4:
            moveRead = int(moveRead.strip())
            if moveRead != 0:
                moves.append(moveRead)
        else:
            roomInfo = moveRead
    textHandle.close()
    return moves

def outputModule():
    """States the module the player is currently in."""
    global module,term,roomInfo,queen,workers,ventShafts,infoPanels,fuel
    print(term.clear())
    print(term.yellow(f"\n\nYou are now in module {module}. {roomInfo}"))
    if module == queen:
        print(term.red(term.blink("You face down the queen, as she stands before you.")))
    if module in workers:
        if fuel > 50:
            print(term.red(term.blink("You stare down a worker alien.")))
            print(term.red("You quickly coat the worker alien in fire."))
            time.sleep(3)
            print(term.yellow("It dies."))
            workers.remove(module)
            fuel = fuel - 100 + random.randint(0,50)
        else:
            print(term.red(term.blink("You stare down a worker alien.")))
            print(term.red("You try to use your flamethrower, but..."))
            time.sleep(3)
            print(term.red("It sputters and goes silent."))
            time.sleep(3)
            print(term.red("The alien approaches you. You can't read the emotion behind its cold eyes."))
    if module in ventShafts:
        print(term.yellow("There is a vent shaft in here."))
    if module in infoPanels:
        print("There is an info panel in here.")

def outputMoves():
    """Prints the allowed moves from the current module"""
    global possibleMoves
    print(term.yellow(f"From here you can move to modules: | "),end='')
    for move in possibleMoves:
        print(term.yellow(str(move)," | "),end='')
    print()

def getAction():
    """Asks the user form an input to then perform that action, e.g. MOVE, SCAN, or view the MAP."""
    global module, lastModule, possibleMoves, term, power,gameMap, num_modules, locked
    validAction = False
    while validAction == False:
        print(term.blue("What do you want to do next? (MOVE, SCANNER, MAP, LOOK)"))
        action = input(term.blue(">>>"))
        command = textParser(action)
        action,detail = command
        if action == "move":
            move = detail
            if move in possibleMoves:
                validAction = True
                lastModule = module
                visitedModules.append(module)
                module = move
                power = power - 1
            else:
                print(term.red("The module must be connected to the current module. Use 'MAP' to see the map. Press ENTER to continue."))
                input()
        elif action == "map":
            validAction = True
            print(term.clear())
            print(term.yellow(gameMap))
            print(term.blue("Press ENTER to continue."))
            input()
        elif action == 'look':
            validAction = True
            print(term.yellow(f"You are in module {module}.\n{roomInfo}"))
            print(term.yellow("Press ENTER to continue"))
        elif action == "scanner":
            validAction = True
            input(term.yellow("Press ENTER to continue"))
        elif action == "lock":
            try:
                newLock = int(input(term.yellow("Enter module to lock: ")))
                if newLock < 0 or newLock > num_modules:
                    print(term.red("Invalid module. Operation failed."))
                if newLock == queen:
                    print(term.red("Unable to lock module. Operation failed."))
                if newLock == locked:
                    print(term.red("That module is already locked! Operation failed."))
                else:
                    locked = newLock
                    print(term.green(f"Aliens cannot get into module {locked}."))
                power_used = 25+5 * random.randint(0,5)
                power = power - power_used
            except:
                print(term.red("Misformed command!"))
        elif action == "panel":
            if detail == "allowed":
                panelInteraction()
            else:
                print(term.red("You can't do that right now!"))
        else:
            print(term.red("Incorrect or misformed action. Read the instructions to see how to form commands correctly."))

def move_queen():
    global num_modules,module,lastModule,locked,queen,won,ventShafts,fuel, alive
    if module == queen:
        movesToMake = random.randint(1,3)
        can_move_to_last_module = False
        while movesToMake > 0:
            escapes = getModulesFrom(queen)
            if module in escapes:
                escapes.remove(module)
            if lastModule in escapes and can_move_to_last_module == False:
                escapes.remove(lastModule)
            if locked in escapes:
                escapes.remove(locked)
            if len(escapes) == 0:
                won = True
                movesToMake = 0
                if fuel >= 100:
                    playerWin()
                else:
                    print(term.yellow("You power up your flamethrower."))
                    time.sleep(2)
                    print(term.red("It sputters weakly."))
                    time.sleep(2)
                    print(term.red("The queen takes a step towards you menacingly."))
                    alive = False

            else:
                if movesToMake == 1:
                    print(term.red("The queen bolts."))
                queen = random.choice(escapes)
                movesToMake = movesToMake - 1
                can_move_to_last_module = True
                while queen in ventShafts:
                    if movesToMake > 1:
                        print(term.red("The queen bolts."))
                        time.sleep(1)
                    print(term.red("We can hear scuttling in the vents."))
                    validMove = False
                    while validMove == False:
                        validMove = True
                        queen = random.randint(1,num_modules)
                        if queen in ventShafts:
                            validMove = False
                    movesToMake = 0

def playerWin():
    time.sleep(4)
    print(term.red("You lock eyes with the queen."))
    time.sleep(3)
    print(term.red("She bolts."))
    time.sleep(2)
    print(term.orange("The door is locked..."))
    time.sleep(2)
    print(term.orange("You power up your flamethrower. You can't make out the queen's emotion from behind her eyes."))




def mainMenu():
    """The main menu of the game, where the player can choose to start a new game, view instructions, or quit."""
    global term
    print(term.clear())
    print(term.yellow("Welcome to Telium!"))
    print(term.blue("1. Play"))
    print(term.blue("2. Story Mode"))
    print(term.blue("3. Instructions"))
    print(term.blue("4. Quit"))
    choice = input(term.blue(">>>"))
    if choice == "1":
        return
    elif choice == "2":
        print("Story mode is not yet implemented. Press ENTER to return to the main menu.")
        input()
        mainMenu()
    elif choice == "3":
        print(term.clear())
        print(term.yellow("Instructions:"))
        print(term.white("You are an engineer on a space station that has been invaded by hostile aliens. Your goal is to trap the alien queen and burn her to death with your flamethrower. You can move between modules of the station, scan for the queen's location, and use your flamethrower to attack. Be careful not to run out of power or fuel, or you will be trapped with the alien and unable to escape. Use the MOVE command to travel to a different module. Good luck - you'll need it."))
        print(term.yellow("Command phrasing:\nMOVE: Enter 'move' or 'm' followed by the module number you want to move to.\nSCANNER: Enter it as 'scanner', then follow the instructions inside of that.\nMAP: Enter it as 'map' to see a map of the station.\nLOOK: Enter 'look' to read the description for the module again."))
        print(term.blue("Press ENTER to return to the main menu."))
        input()
        mainMenu()
    elif choice == "4":
        sys.exit()
    else:
        print(term.red("Invalid choice. Please enter 1, 2, 3, or 4. Press ENTER to continue."))
        input()
        mainMenu()

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
        scannerCalled()
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

def spawnNPCs():
    global num_modules, queen, ventShafts, infoPanels, workers
    moduleSet = []
    for counter in range(2,num_modules+1):
        moduleSet.append(counter)
    random.shuffle(moduleSet)
    i = 0
    queen = moduleSet[i]
    for counter in range(0,3):
        i=i+1
        ventShafts.append(moduleSet[i])
    for counter in range(0,2):
        i=i+1
        infoPanels.append(moduleSet[i])
    for counter in range(0,3):
        i=i+1
        workers.append(moduleSet[i])

def scannerCalled():
    global power, fuel,workers,possibleMoves, infoPanels,ventShafts,queen
    command = input(term.yellow("Scanner ready. Enter command (LOCK, POWER, FUEL, LIFEFORMS, SCAN): "))
    if command.lower() == "lock":
        lock()
    elif command.lower() == "power":
        print(term.yellow(f"The station has {power} left. Better not reach 0. "))
    elif command.lower() == "fuel":
        print(term.yellow(f"Your flamethrower has {fuel} fuel left. There are some banks of fuel cells should you run out, but best to not be caught out."))
    elif command.lower() == "lifeforms":
        print(term.yellow(f"There are {len(workers+1)} alien lifeforms aboard the ship."))
    elif command.lower() == "scan":
        if power > 25:
            print(term.yellow("Which module do you want to scan? "))
            toScan = input(term.blue(">>>"))
            if toScan in possibleMoves:
                print(term.yellow(f"Module {toScan}: "))
                if toScan in infoPanels:
                   print(term.yellow("1 X Information Panel"))
                if toScan in ventShafts:
                   print(term.yellow("1 X Ventilation Shaft"))
                if toScan in workers:
                   print(term.yellow("1 X Worker Alien"))
                if queen == toScan:
                   print(term.red("1 X Telium Queen"))
                power = power - 25
            else:
                print(term.orange("Must be connected to the current module!"))
        else:
            print(term.orange("You don't have enough power to perform that action!"))
    else:
        print(term.red("Your scanner reads: 'UNRECOGNISED COMMAND.' Read the game's instructions for how to form commands."))

def lock():
    global num_modules,power,locked
    try:
        newLock = int(input(term.yellow("Enter module to lock: ")))
        if newLock < 0 or newLock > num_modules:
            print(term.red("Invalid module. Operation failed."))
        if newLock == queen:
            print(term.red("Unable to lock module. Operation failed."))
        if newLock == locked:
            print(term.red("That module is already locked! Operation failed."))
        else:
            locked = newLock
            print(term.green(f"Aliens cannot get into module {locked}."))
        power_used = 25+5 * random.randint(0,5)
        power = power - power_used
    except:
        print(term.red("Misformed command!"))

def checkVents():
    global num_modules,module,ventShafts,fuel,lastModule
    if module in ventShafts:
        time.sleep(5)
        print(term.yellow("There is a bank of fuel cells here. You load one into your flamethrower."))
        time.sleep(3)
        fuelGained = random.randint(10,100)
        print(term.yellow(f"Fuel was {fuel}, now reading {fuel+fuelGained}."))
        fuel = fuel+fuelGained
        time.sleep(4)
        print(term.red("The doors suddenly lock shut."))
        time.sleep(1)
        print(term.red("What is happening to the station??"))
        time.sleep(0.5)
        print(term.red("We have to climb into the ventilation shaft."))
        time.sleep(0.5)
        print(term.red("We don't know where we're going"))
        time.sleep(0.5)
        print(term.red("What if it doesn't go anywhere?"))
        time.sleep(0.5)
        print(term.red("There's no time!"))
        time.sleep(0.25)
        print(term.clear())
        print(term.red("We climb in and find ourselves sliding down."))
        time.sleep(3)
        lastModule=module
        module = random.randint(1,num_modules)
        while module in ventShafts:
            module = random.randint(1,num_modules)
        loadModule()

def intuition():
    #prints output based on connected modules
    global possibleMoves,workers,ventShafts,queen,infoPanels
    worker = False
    vents = False
    panel = False
    for connected_module in possibleMoves:
        if connected_module in workers:
            if worker == False:
                print(term.orange("I can hear something scuttling!"))
                worker = True
            else:
                print(term.red("The scuttling... it's coming from more than one room..."))
        if connected_module in ventShafts:
                if vents == False:
                    print(term.orange("I can feel cool air!"))
                    vents = True
                else:
                    print(term.orange("Quiet! There's rushing air coming from more than one door here..."))
        if connected_module == queen:
            print(term.red("'Shh! Did you hear that?'"))
        if connected_module in infoPanels:
            if panel == False:
                print(term.blink(term.yellow("There is a panel near here. We could use it to find lifeforms.")))
                panel = True
            else:
                print(term.yellow("If I remember right, there's more than one panel around here..."))

def panelInteraction():
    global queen, power
    string = f"The queen is in module {queen}."
    for i in range(len(string)):
        print(term.green(string[i]),end="")
        time.sleep(random.random(0,0.5))
    print("\n")
    time.sleep(1)
    print(term.red(term.blink("The station just lost 50 power.")))
    power = power - 50
        

mainMenu()
spawnNPCs()

print("Telium is located in module",queen)
print("Ventilation shafts in modules:",ventShafts)
print("Information panels in modules:",infoPanels)
print("Worker aliens in modules:",workers)

while alive and not won and power > 0:
    loadModule()
    outputMoves()
    intuition()
    getAction()

if won == True:
    print(term.yellow("The queen is trapped and you burn it to death with your flamethrower."))
    print(term.blink(term.green_on_white("Game over: YOU WIN!")))
if alive == False:
    print(term.red("you died."))
    print(term.blink(term.white_on_firebrick3("GAME OVER.")))
if power <= 0:
    print(term.red("You ran out of power. Unable to move or use the scanner, you are trapped in the station, with a hostile alien. Alone and powerless, you turn around to see the queen staring at you. You are too weak to fight back."))
    time.sleep(3)
    print(term.blink(term.white_on_firebrick3("YOU DIED. GAME OVER.")))


time.sleep(5)
print(term.orange("Press ENTER to quit."))
input()