#Embedded file name: scripts/client/gui/game_control/RenalsController.py
from operator import itemgetter
import BigWorld
import Event
from gui.shared.ItemsCache import g_itemsCache
from gui.shared.utils.requesters.ItemsRequester import REQ_CRITERIA
from helpers import time_utils

class RentalsController(object):
    onRentChangeNotify = Event.Event()

    def init(self):
        self.__rentNotifyTimeCallback = None
        self.__vehicleForUpdate = None

    def fini(self):
        self.stop()

    def start(self):
        g_itemsCache.onSyncCompleted += self._update
        if self.__rentNotifyTimeCallback is None:
            self.__startRentTimeNotifyCallback()

    def stop(self):
        self.__clearRentTimeNotifyCallback()
        self.__vehicleForUpdate = None
        self.onRentChangeNotify.clear()
        g_itemsCache.onSyncCompleted -= self._update

    def _update(self, *args):
        if self.__rentNotifyTimeCallback is None:
            self.__startRentTimeNotifyCallback()

    def __startRentTimeNotifyCallback(self):
        self.__clearRentTimeNotifyCallback()
        self.__vehicleForUpdate = None
        rentedVehicles = g_itemsCache.items.getVehicles(REQ_CRITERIA.EMPTY | REQ_CRITERIA.VEHICLE.ACTIVE_RENT).values()
        notificationList = []
        for vehicle in rentedVehicles:
            delta = vehicle.rentLeftTime
            if delta > time_utils.ONE_DAY:
                period = time_utils.ONE_DAY
            elif delta > time_utils.ONE_HOUR:
                period = time_utils.ONE_HOUR
            else:
                period = delta
            notificationList.append((vehicle.intCD, delta % period or period))

        if len(notificationList) > 0:
            self.__vehicleForUpdate, nextRentNotification = min(notificationList, key=itemgetter(1))
            nextRentNotification = max(nextRentNotification, 0)
        else:
            return
        self.__rentNotifyTimeCallback = BigWorld.callback(nextRentNotification, self.__notifyRentTime)

    def __notifyRentTime(self):
        self.onRentChangeNotify(self.__vehicleForUpdate)
        self.__startRentTimeNotifyCallback()

    def __clearRentTimeNotifyCallback(self):
        if self.__rentNotifyTimeCallback is not None:
            BigWorld.cancelCallback(self.__rentNotifyTimeCallback)
            self.__rentNotifyTimeCallback = None
