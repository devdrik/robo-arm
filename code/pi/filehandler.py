

class FileHandler():

    def __init__(self):
        self.velocityIdentifier = 'vel'

    def saveToFile(self, fname, angles):
        with open("moveFiles/" + fname, "w") as f:
            for angle in angles:
                if angle[0] == self.velocityIdentifier:
                    f.write(f'{angle[0]}:{angle[1]}\n')
                else:
                    f.write("{},{},{},{},{}\n".format(angle[0],angle[1],angle[2],angle[3],angle[4]))


    def getAnglesFromFile(self, fname):
        with open("moveFiles/" + fname) as f:
            lines = f.readlines()
        angles = []
        # print(lines)
        for line in lines:
            lineValues = []
            if line.startswith(self.velocityIdentifier):
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