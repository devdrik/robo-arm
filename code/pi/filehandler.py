

class FileHandler():

    def __init__(self):
        self.__velocityIdentifier = 'vel'
        self.__pauseIdentifier = 'pause'

    def saveToFile(self, fname, actionsList):
        with open("moveFiles/" + fname, "w") as f:
            for action in actionsList:
                if action[0] == self.__velocityIdentifier or action[0] == self.__pauseIdentifier:
                    f.write(f'{action[0]}:{action[1]}\n')
                else:
                    f.write("{},{},{},{},{}\n".format(action[0],action[1],action[2],action[3],action[4]))

    def getActionsFromFile(self, fname):
        with open("moveFiles/" + fname) as f:
            lines = f.readlines()
        angles = []
        # print(lines)
        for line in lines:
            lineValues = []
            if line.startswith(self.__velocityIdentifier) or line.startswith(self.__pauseIdentifier):
                values = line.split(':')
                lineValues.append(values[0])
                lineValues.append(float(values[1]))
            else:
                for value in line.split(','):
                    if value.endswith("\n"):
                        value=value[:-1]
                    lineValues.append(float(value))
            angles.append(lineValues)
        return angles