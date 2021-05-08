from abc import ABC, abstractmethod

class IServo(ABC):

    @abstractmethod
    def getAngle(self):
        pass

    @abstractmethod
    def setAngle(self, angle):
        pass
