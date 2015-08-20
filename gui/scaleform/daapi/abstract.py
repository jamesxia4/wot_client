#Embedded file name: scripts/client/gui/Scaleform/daapi/abstract.py
from debug_utils import LOG_DEBUG

class StatsStorageMeta(object):

    def as_setExperienceS(self, experience):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setExperience(experience)

    def as_setTankmanIdS(self, id):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setTankmanId(id)

    def as_setCreditsS(self, credits):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setCredits(credits)

    def as_setGoldS(self, gold):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setGold(gold)

    def as_setPremiumS(self, premium):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setPremium(premium)

    def as_setVehicleS(self, vehicle):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setVehicle(vehicle)

    def as_setPlayerSpeakingS(self, dbId, isSpeak, isSelf):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setPlayerSpeaking(dbId, isSpeak, isSelf)

    def as_setAccountAttrsS(self, attrs):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setAccountAttrs(attrs)

    def as_setDenunciationsCountS(self, denunciationsCount):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setDenunciationsCount(denunciationsCount)

    def as_setNationsS(self, nations):
        if self.flashObject is None:
            LOG_DEBUG('flash object can`t be None!')
        else:
            self.flashObject.as_setNations(nations)
