#Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/FalloutBattleSelectorWindow.py
from adisp import process
from constants import FALLOUT_BATTLE_TYPE, QUEUE_TYPE
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.game_control import getFalloutCtrl
from gui.prb_control.context import prb_ctx
from gui.prb_control.prb_helpers import prbDispatcherProperty
from gui.shared import events, EVENT_BUS_SCOPE
from helpers import i18n
from gui.Scaleform.daapi.view.meta.FalloutBattleSelectorWindowMeta import FalloutBattleSelectorWindowMeta
from gui.Scaleform.genConsts.FALLOUT_ALIASES import FALLOUT_ALIASES
from gui.Scaleform.locale.FALLOUT import FALLOUT
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.shared.formatters.text_styles import promoSubTitle, main
from gui.shared.utils.functions import makeTooltip
from gui import makeHtmlString
_TOOLTIP_DATA = {FALLOUT_ALIASES.TOOLTIP_DATA_DOMINATION: (TOOLTIPS.BATTLESELECTORWINDOW_TOOLTIP_DOMINATION_SELECTBTN_HEADER, TOOLTIPS.BATTLESELECTORWINDOW_TOOLTIP_DOMINATION_SELECTBTN_BODY, None),
 FALLOUT_ALIASES.TOOLTIP_DATA_MULITEAM: (TOOLTIPS.BATTLESELECTORWINDOW_TOOLTIP_MULTITEAM_SELECTBTN_HEADER, TOOLTIPS.BATTLESELECTORWINDOW_TOOLTIP_MULTITEAM_SELECTBTN_BODY, None)}

class FalloutBattleSelectorWindow(FalloutBattleSelectorWindowMeta):

    def __init__(self, ctx = None):
        super(FalloutBattleSelectorWindow, self).__init__(ctx)

    @prbDispatcherProperty
    def prbDispatcher(self):
        return None

    def _populate(self):
        super(FalloutBattleSelectorWindow, self)._populate()
        self.addListener(events.HideWindowEvent.HIDE_BATTLE_SESSION_WINDOW, self.__handleFalloutWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        self.as_setInitDataS({'windowTitle': FALLOUT.BATTLESELECTORWINDOW_TITLE,
         'headerTitleStr': promoSubTitle(FALLOUT.BATTLESELECTORWINDOW_HEADERTITLESTR),
         'headerDescStr': main(FALLOUT.BATTLESELECTORWINDOW_HEADERDESC),
         'dominationBattleTitleStr': promoSubTitle(FALLOUT.BATTLESELECTORWINDOW_DOMINATION_TITLE),
         'dominationBattleDescStr': main(FALLOUT.BATTLESELECTORWINDOW_DOMINATION_DESCR),
         'dominationBattleBtnStr': FALLOUT.BATTLESELECTORWINDOW_DOMINATIONBATTLEBTNLBL,
         'multiteamTitleStr': promoSubTitle(FALLOUT.BATTLESELECTORWINDOW_MULTITEAM_TITLE),
         'multiteamDescStr': main(FALLOUT.BATTLESELECTORWINDOW_MULTITEAM_DESCR),
         'multiteamBattleBtnStr': FALLOUT.BATTLESELECTORWINDOW_MULTITEAMBATTLEBTNLBL,
         'bgImg': RES_ICONS.MAPS_ICONS_LOBBY_FALLOUTBATTLESELECTORBG})

    def _dispose(self):
        self.removeListener(events.HideWindowEvent.HIDE_BATTLE_SESSION_WINDOW, self.__handleFalloutWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        super(FalloutBattleSelectorWindow, self)._dispose()

    def onWindowMinimize(self):
        self.destroy()

    def onWindowClose(self):
        self.__leaveFallout()

    def onDominationBtnClick(self):
        getFalloutCtrl().setBattleType(FALLOUT_BATTLE_TYPE.CLASSIC)
        self.onWindowMinimize()

    def onMultiteamBtnClick(self):
        getFalloutCtrl().setBattleType(FALLOUT_BATTLE_TYPE.MULTITEAM)
        self.onWindowMinimize()

    def getTooltipForBtn(self, tooltipKey):
        params = _TOOLTIP_DATA[tooltipKey]
        return self.__getTooltipData(*params)

    def __getTooltipData(self, header, body, icon = None):
        if icon is not None:
            htmlPrebattleTag = 'html_templates:lobby/prebattle/'
            icon = makeHtmlString(htmlPrebattleTag, 'selectorWindowTooltipImg') % icon
        else:
            icon = ''
        return makeTooltip(header, icon + '\n' + i18n.makeString(body))

    def __handleFalloutWindowHide(self, _):
        self.destroy()

    @process
    def __leaveFallout(self):
        yield self.prbDispatcher.join(prb_ctx.JoinModeCtx(QUEUE_TYPE.RANDOMS))
