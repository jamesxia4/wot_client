#Embedded file name: scripts/client/gui/shared/gui_items/processors/common.py
import BigWorld
from debug_utils import *
from gui.SystemMessages import SM_TYPE
from gui.shared import g_itemsCache
from gui.shared.utils.gui_items import formatPrice, formatGoldPrice
from gui.shared.gui_items.processors import Processor, makeI18nError, makeI18nSuccess, plugins

class TankmanBerthsBuyer(Processor):

    def __init__(self, berthsPrice, berthsCount):
        super(TankmanBerthsBuyer, self).__init__((plugins.MessageInformator('barracksExpandNotEnoughMoney', activeHandler=lambda : not plugins.MoneyValidator(berthsPrice).validate().success), plugins.MessageConfirmator('barracksExpand', ctx={'price': berthsPrice[1],
          'count': berthsCount}), plugins.MoneyValidator(berthsPrice)))
        self.berthsPrice = berthsPrice

    def _errorHandler(self, code, errStr = '', ctx = None):
        if len(errStr):
            return makeI18nError('buy_tankmen_berths/%s' % errStr)
        return makeI18nError('buy_tankmen_berths/server_error')

    def _successHandler(self, code, ctx = None):
        return makeI18nSuccess('buy_tankmen_berths/success', money=formatPrice(self.berthsPrice), type=SM_TYPE.PurchaseForGold)

    def _request(self, callback):
        LOG_DEBUG('Make server request to buy tankman berths')
        BigWorld.player().stats.buyBerths(lambda code: self._response(code, callback))


class PremiumAccountBuyer(Processor):

    def __init__(self, period, price, arenaUniqueID = 0):
        self.wasPremium = g_itemsCache.items.stats.isPremium
        localKey = 'premiumContinueConfirmation' if self.wasPremium else 'premiumBuyConfirmation'
        super(PremiumAccountBuyer, self).__init__((plugins.MessageConfirmator(localKey, ctx={'days': int(period),
          'gold': BigWorld.wg_getGoldFormat(price)}), plugins.MoneyValidator((0, price))))
        self.premiumPrice = price
        self.period = period
        self.arenaUniqueID = arenaUniqueID

    def _errorHandler(self, code, errStr = '', ctx = None):
        if len(errStr):
            return makeI18nError('premium/%s' % errStr, period=self.period)
        return makeI18nError('premium/server_error', period=self.period)

    def _successHandler(self, code, ctx = None):
        localKey = 'premium/continueSuccess' if self.wasPremium else 'premium/buyingSuccess'
        return makeI18nSuccess(localKey, period=self.period, money=formatGoldPrice(self.premiumPrice), type=SM_TYPE.PurchaseForGold)

    def _request(self, callback):
        LOG_DEBUG('Make server request to buy premium account', self.period, self.premiumPrice)
        BigWorld.player().stats.upgradeToPremium(self.period, self.arenaUniqueID, lambda code: self._response(code, callback))


class GoldToCreditsExchanger(Processor):

    def __init__(self, gold):
        self.gold = gold
        self.credits = int(gold) * g_itemsCache.items.shop.exchangeRate
        super(GoldToCreditsExchanger, self).__init__(plugins=(plugins.HtmlMessageConfirmator('exchangeGoldConfirmation', 'html_templates:lobby/dialogs', 'confirmExchange', {'primaryCurrencyAmount': BigWorld.wg_getGoldFormat(self.gold),
          'resultCurrencyAmount': BigWorld.wg_getIntegralFormat(self.credits)}), plugins.MoneyValidator((0, self.gold))))

    def _errorHandler(self, code, errStr = '', ctx = None):
        if len(errStr):
            return makeI18nError('exchange/%s' % errStr, gold=self.gold)
        return makeI18nError('exchange/server_error', gold=self.gold)

    def _successHandler(self, code, ctx = None):
        return makeI18nSuccess('exchange/success', gold=BigWorld.wg_getGoldFormat(self.gold), credits=formatPrice((self.credits, 0)), type=SM_TYPE.FinancialTransactionWithGold)

    def _request(self, callback):
        LOG_DEBUG('Make server request to exchange gold to credits')
        BigWorld.player().stats.exchange(self.gold, lambda code: self._response(code, callback))


class FreeXPExchanger(Processor):

    def __init__(self, xp, vehiclesCD, freeConversion = False):
        rate = g_itemsCache.items.shop.freeXPConversion
        self.xp = xp
        self.__freeConversion = bool(freeConversion)
        self.gold = round(rate[1] * xp / rate[0]) if not freeConversion else 0
        self.vehiclesCD = vehiclesCD
        super(FreeXPExchanger, self).__init__(plugins=(self.__makeConfirmator(), plugins.MoneyValidator((0, self.gold)), plugins.EliteVehiclesValidator(self.vehiclesCD)))

    def _errorHandler(self, code, errStr = '', ctx = None):
        if len(errStr):
            return makeI18nError('exchangeXP/%s' % errStr, xp=BigWorld.wg_getIntegralFormat(self.xp))
        return makeI18nError('exchangeXP/server_error', xp=BigWorld.wg_getIntegralFormat(self.xp))

    def _successHandler(self, code, ctx = None):
        return makeI18nSuccess('exchangeXP/success', gold=BigWorld.wg_getGoldFormat(self.gold), xp=BigWorld.wg_getIntegralFormat(self.xp), type=SM_TYPE.FinancialTransactionWithGold)

    def _request(self, callback):
        LOG_DEBUG('Make server request to exchange xp for credits')
        BigWorld.player().stats.convertToFreeXP(self.vehiclesCD, self.xp, lambda code: self._response(code, callback), int(self.__freeConversion))

    def __makeConfirmator(self):
        xpLimit = g_itemsCache.items.shop.freeXPConversionLimit
        extra = {'resultCurrencyAmount': BigWorld.wg_getIntegralFormat(self.xp),
         'primaryCurrencyAmount': BigWorld.wg_getGoldFormat(self.gold)}
        if self.__freeConversion:
            sourceKey = 'XP_EXCHANGE_FOR_FREE'
            extra['freeXPLimit'] = BigWorld.wg_getIntegralFormat(xpLimit)
        else:
            sourceKey = 'XP_EXCHANGE_FOR_GOLD'
        return plugins.HtmlMessageConfirmator('exchangeXPConfirmation', 'html_templates:lobby/dialogs', 'confirmExchangeXP', extra, sourceKey=sourceKey)
