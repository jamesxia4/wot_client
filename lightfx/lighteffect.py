#Embedded file name: scripts/client/LightFx/LightEffect.py
import BigWorld
import weakref
import Event
ACTION_MORPH = 1
ACTION_PULSE = 2
ACTION_COLOR = 3

class OneLightAction:

    def __init__(self, lightDescription, color, action):
        self.lightDescription = lightDescription
        self.color = color
        self.action = action


class LightEffect:

    def __init__(self, name, lightActions, duration = None):
        self.name = name
        self.lightActions = lightActions
        self.__duration = duration
        self.__eventManager = Event.EventManager()
        self.onStop = Event.Event(self.__eventManager)
        self.__onStopCallbackId = None
        self.__isRunning = False

    def isRunning(self):
        return self.__isRunning

    def destroy(self):
        if self.__onStopCallbackId is not None:
            BigWorld.cancelCallback(self.__onStopCallbackId)
            self.__onStopCallbackId = None
        self.__eventManager.clear()

    def start(self):
        if self.__onStopCallbackId is not None:
            BigWorld.cancelCallback(self.__onStopCallbackId)
            self.__onStopCallbackId = None
        if self.__duration is not None:
            self.__onStopCallbackId = BigWorld.callback(self.__duration, self.stop)
        self.__isRunning = True

    def stop(self):
        if self.__onStopCallbackId is not None:
            BigWorld.cancelCallback(self.__onStopCallbackId)
            self.__onStopCallbackId = None
        self.onStop(self)
        self.__isRunning = False
