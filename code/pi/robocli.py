import time

class RoboCLI():

    def __init__(self, robo, fileHandler):
        self.robo = robo
        self.fileHandler = fileHandler
        self.actions = []
    
    def startTeachingCli(self):
        self.actions = []
        while True:
            self.robo.startTeachMode()
            menu = self.__getMenu()
            inp = input(menu)
            try:
                if inp == 'q':
                    break
                inp = int(inp)
            except:
                continue
            if inp == 1:
                self.__setPosition()
            elif inp == 2:
                self.__saveToFile()
            elif inp == 3:
                self.__apendFromFile()
            elif inp == 4:
                self.__runActions()
            elif inp == 5:
                self.actions = []
            elif inp == 6:
                self.__setVelocity()
            elif inp == 7:
                self.__addPause()
            elif inp == 8:
                self.__deleteLastEntry()
            elif inp == 9:
                self.__showEntries()

    def __setPosition(self):
        action = self.robo.getAngles()
        self.actions.append(action)
        print(action)

    def __saveToFile(self):
        fname = input("enter filename: ")
        self.fileHandler.saveToFile(fname, self.actions)

    def __apendFromFile(self):
        fname = input("enter filename: ")
        try:
            actionsFromFile = self.fileHandler.getActionsFromFile(fname)
            self.actions.extend(actionsFromFile)
        except:
            print("Error, file not existent?")

    def __runActions(self):
        self.robo.startPositionMode()
        self.robo.setVelocity(self.__getVelocityInput())
        for action in self.actions:
            if action[0] == 'vel':
                self.robo.setVelocity(action[1])
            elif action[0] == 'pause':
                time.sleep(action[1])
            else:
                self.robo.setAnglesBlocking(action)
                # self.robo.setAngles(angle)
                # time.sleep(0.1)

    def __setVelocity(self):
        entry = []
        entry.append('vel')
        entry.append(self.__getVelocityInput())
        self.actions.append(entry)

    def __addPause(self):
        entry = []
        entry.append('pause')
        entry.append(self.__getFloatInput("enter pause in [s]: "))
        self.actions.append(entry)


    def __getMenu(self):
        menu = ""
        for option in self.__getOptions():
            menu += option + '\n'
        menu += "your choice: "
        return menu

    def __getOptions(self):
        options=[
            "[1] set Position",
            "[2] save to file",
            "[3] read from file (append)",
            "[4] run actions",
            "[5] clear angles",
            "[6] change velocity",
            "[7] add pause",
            "[8] remove last entry",
            "[9] show entries",
            "[q] end"
        ]
        return options

    def __getVelocityInput(self):
        while True:
            vel = input("enter velocity: ")
            try:
                vel = int(vel)
            except:
                print("Not a number, try again")
                continue
            break
        return vel

    def __getFloatInput(self, request="enter float value: "):
        while True:
            val = input(request)
            try:
                val = float(val)
            except:
                print("Not a number, try again")
                continue
            break
        return val

    def __deleteLastEntry(self):
        self.actions.pop()
    
    def __showEntries(self):
        for entry in self.actions:
            print(entry)
