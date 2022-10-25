from constant import * 
import math

class UltrasonicSensor(object):
    __staticSpeedOfLight = 340

    def __init__(self):
        # ToDo: Topic fuer jeden Sensor festlegen
        self.__TimeMeasurement = 0
        self.__Distance = 0

    def WriteTime(self, timeMeasurement):
        self.__TimeMeasurement = timeMeasurement
        self.__Distance = UltrasonicSensor.__CalculateDistance(self.__TimeMeasurement)
        # ToDo: KalmanFilter
        
    def GetDistance(self):
        return self.__Distance
        # ToDo: Variablen Klassen ueberpruefen mit Zugriffsberechtigung

    @staticmethod
    def GetSpeedOfLight():
        return UltrasonicSensor.__staticSpeedOfLight

    @staticmethod
    def __CalculateDistance(timeMeasurementCD):
        return (UltrasonicSensor.__staticSpeedOfLight * timeMeasurementCD) / 2000

    @staticmethod
    def CalculateSpeedOfLight(temperatureRef, timeMeasurementRef):
        UltrasonicSensor.__staticSpeedOfLight = FACTOR_SPEED_OF_LIGHT * math.sqrt(temperatureRef)
        currentStep = 0
        previousStep = 0
        while True:
            if timeMeasurementRef == 0:
                break
            
            distanceRef = UltrasonicSensor.__CalculateDistance(timeMeasurementRef)

            if distanceRef > DISTANCE_REF:
                UltrasonicSensor.__staticSpeedOfLight -= CHANGE_SPEED_OF_LIGHT
                currentStep = 1
            elif distanceRef < DISTANCE_REF:
                UltrasonicSensor.__staticSpeedOfLight += CHANGE_SPEED_OF_LIGHT
                currentStep = 2
            else:
                break

            if currentStep != previousStep and previousStep != 0:
                break

            previousStep = currentStep

