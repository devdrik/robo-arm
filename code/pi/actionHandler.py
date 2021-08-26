import time

class ActionHandler():

    def __init__(self, robo, fileHandler):
        self.robo = robo
        self.fileHandler = fileHandler
        self.actions = []

    def setPosition(self):
        action = self.robo.getAngles()
        self.actions.append(action)
        print(action)

    def saveToFile(self, fname):
        self.fileHandler.saveToFile(fname, self.actions)

    def appendFromFile(self, fname):
        try:
            actionsFromFile = self.fileHandler.getActionsFromFile(fname)
            self.actions.extend(actionsFromFile)
        except:
            print("Error, file not existent? fname: ", fname)

    def runActions(self, velocity):
        self.robo.startPositionMode()
        self.robo.setVelocity(velocity)
        for action in self.actions:
            if action[0] == 'vel':
                self.robo.setVelocity(action[1])
            elif action[0] == 'pause':
                time.sleep(action[1])
            else:
                self.robo.setAnglesBlocking(action)
                # self.robo.setAngles(angle)
                # time.sleep(0.1)

    def setVelocity(self, velocity: int):
        entry = []
        entry.append('vel')
        entry.append(velocity)
        self.actions.append(entry)

    def addPause(self, pauseInSeconds: float):
        entry = []
        entry.append('pause')
        entry.append(pauseInSeconds)
        self.actions.append(entry)

    def deleteLastEntry(self):
        self.actions.pop()
    
    def showEntries(self):
        for entry in self.actions:
            print(entry)

    def clearActions(self):
        self.actions = []