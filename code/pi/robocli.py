import time

class RoboCLI():

    def __init__(self, robo, fileHandler):
        self.robo = robo
        self.fileHandler = fileHandler
    
    def startCli(self):
        actions = []
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
                action = self.robo.getAngles()
                actions.append(action)
                print(action)
            elif inp == 2:
                fname = input("enter filename: ")
                self.fileHandler.saveToFile(fname, actions)
            elif inp == 3:
                fname = input("enter filename: ")
                try:
                    actionsFromFile = self.fileHandler.getActionsFromFile(fname)
                    actions.extend(actionsFromFile)
                except:
                    print("Error, filename not existent?")
            elif inp == 4:
                self.robo.startPositionMode()
                self.robo.setVelocity(self.__getVelocityInput())
                for action in actions:
                    if action[0] == 'vel':
                        self.robo.setVelocity(action[1])
                    elif action[0] == 'pause':
                        time.sleep(action[1])
                    else:
                        self.robo.setAnglesBlocking(action)
                        # self.robo.setAngles(angle)
                        time.sleep(0.1)
            elif inp == 5:
                actions = []
            elif inp == 6:
                entry = []
                entry.append('vel')
                entry.append(self.__getVelocityInput())
                actions.append(entry)
            elif inp == 7:
                entry = []
                entry.append('pause')
                entry.append(self.__getFloatInput("enter pause in [s]: "))
                actions.append(entry)

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
            "[4] play angles",
            "[5] clear angles",
            "[6] change velocity",
            "[7] add pause",
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