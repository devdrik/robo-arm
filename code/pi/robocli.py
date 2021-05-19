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
                    angles = anglesFromFile
                except:
                    print("Error, filename not existent?")
            elif inp == 4:
                self.robo.startPositionMode()
                self.robo.setVelocity(self.__getVelocityInput())
                for angle in angles:
                    self.robo.setAnglesBlocking(angle)
                    # self.robo.setAngles(angle)
                    time.sleep(0.5)

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
            "[3] read from file",
            "[4] play angles",
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