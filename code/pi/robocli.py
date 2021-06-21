import time

class RoboCLI():

    def __init__(self, robo, fileHandler):
        self.robo = robo
        self.fileHandler = fileHandler
    
    def startCli(self):
        angles = []
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
                angle = self.robo.getAngles()
                angles.append(angle)
                print(angle)
            elif inp == 2:
                fname = input("enter filename: ")
                self.fileHandler.saveToFile(fname, angles)
            elif inp == 3:
                fname = input("enter filename: ")
                try:
                    anglesFromFile = self.fileHandler.getAnglesFromFile(fname)
                    angles.extend(anglesFromFile)
                except:
                    print("Error, filename not existent?")
            elif inp == 4:
                self.robo.startPositionMode()
                self.robo.setVelocity(self.__getVelocityInput())
                for angle in angles:
                    if angle[0] == 'vel':
                        self.robo.setVelocity(angle[1])
                    else:
                        self.robo.setAnglesBlocking(angle)
                        # self.robo.setAngles(angle)
                        time.sleep(0.1)
            elif inp == 5:
                angles = []
            elif inp == 6:
                entry = []
                entry.append('vel')
                entry.append(self.__getVelocityInput())
                angles.append(entry)
            elif inp == 7:
                entry = []
                entry.append('pause')
                entry.append(self.__getFloatInput("enter pause in [s]"))
                angles.append(entry)

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