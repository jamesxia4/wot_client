#Embedded file name: scripts/client/gui/prb_control/formatters/windows.py
from gui.Scaleform.locale.PREBATTLE import PREBATTLE
from gui.shared import actions
from gui.LobbyContext import g_lobbyContext
from gui.server_events import g_eventsCache
from predefined_hosts import g_preDefinedHosts

class SwitchPeripheryCtx(object):

    def getHeader(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError

    def getSelectServerLabel(self):
        raise NotImplementedError

    def getApplySwitchLabel(self):
        raise NotImplementedError

    def getExtraChainSteps(self):
        raise NotImplementedError

    def getForbiddenPeripherieIDs(self):
        raise NotImplementedError


class SwitchPeripheryCompanyCtx(SwitchPeripheryCtx):

    def getHeader(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_COMPANY_HEADER

    def getDescription(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_COMPANY_DESCRIPTION

    def getSelectServerLabel(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_COMPANY_SELECTSERVERLABEL

    def getApplySwitchLabel(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_COMPANY_APPLYSWITCHLABEL

    def getExtraChainSteps(self):
        return [actions.ShowCompanyWindow()]

    def getForbiddenPeripherieIDs(self):
        hostsSet = set((x[3] for x in g_preDefinedHosts.getSimpleHostsList(g_preDefinedHosts.hostsWithRoaming())))
        for peripheryID in g_eventsCache.getCompanyBattles().peripheryIDs:
            if peripheryID in hostsSet:
                hostsSet.remove(peripheryID)

        return hostsSet


class SwitchPeripheryFortCtx(SwitchPeripheryCtx):

    def getHeader(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_FORT_HEADER

    def getDescription(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_FORT_DESCRIPTION

    def getSelectServerLabel(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_FORT_SELECTSERVERLABEL

    def getApplySwitchLabel(self):
        return PREBATTLE.SWITCHPERIPHERYWINDOW_FORT_APPLYSWITCHLABEL

    def getExtraChainSteps(self):
        return None

    def getForbiddenPeripherieIDs(self):
        return g_lobbyContext.getServerSettings().getForbiddenSortiePeripheryIDs()
