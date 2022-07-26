import json
with open('dataItems.json', 'r') as file:
    src = file.read()
itemsData = json.loads(src)

class Season():
    def __init__(self, SeasonInfo):
        self.SeasonInfo = SeasonInfo
        # for k,v in SeasonInfo:
        #     setattr(self, k,v)
        self.seasonNumber = self.SeasonInfo['seasonNumber']
        self.seasonXp = self.SeasonInfo['seasonXp']
        self.seasonLevel = self.SeasonInfo['seasonLevel']
        self.purchasedVIP = self.SeasonInfo['purchasedVIP']
        self.numRoyalRoyales = self.SeasonInfo['numRoyalRoyales']
        self.numWins = self.SeasonInfo['numWins']
        self.numHighBracket = self.SeasonInfo['numHighBracket']
        self.numLowBracket = self.SeasonInfo['numLowBracket']

    def get_info(self):
        return {
                'seasonNumber': self.seasonNumber,
                'seasonXp': self.seasonXp,
                'seasonLevel': self.seasonLevel,
                'purchasedVIP': self.purchasedVIP,
                'numRoyalRoyales': self.numRoyalRoyales,
                'numWins': self.numWins,
                'numHighBracket': self.numHighBracket,
                'numLowBracket': self.numLowBracket
                }

class StatsAttributes():
    def __init__(self,Attributes):
        self.AttributesInfo = Attributes['attributes']
        self.season_num = self.AttributesInfo['season_num']
        self.bookLevel = self.AttributesInfo['book_level']
        self.lifetimeWins = self.AttributesInfo['lifetime_wins']
        self.level = self.AttributesInfo['level']
        self.accountLevel = self.AttributesInfo['accountLevel']
        self.past_seasons = [Season(season).get_info() for season in self.AttributesInfo['past_seasons']]

class Stats():
    def __init__(self, stats):
        self.__stats = stats['stats']
        self.Attributes = StatsAttributes(self.__stats)

class Item():
    def __init__(self, ItemInfo):
        self.ItemInfo = ItemInfo
        self.ItemAttributes = self.ItemInfo['attributes']
        self.templateId = self.ItemInfo['templateId'].split(':')
        self.id = self.templateId[1]
        self.type = self.templateId[0]
        self.item_seen = False
        if 'item_seen' in self.ItemAttributes:
            self.item_seen = self.ItemAttributes['item_seen']

    def get_info(self):
        if self.item_seen:

            if self.type in ('AthenaCharacter', 'AthenaPickaxe'):
                return itemsData[self.id]

class Profile():
    def __init__(self, response):
        self.__data = response['profileChanges'][0]['profile']
        self.created = self.__data['created']
        self.updated = self.__data['updated']
        self.accountId = self.__data['accountId']
        self.profileId = self.__data['profileId']
        self.Stats = Stats(self.__data)
        self.Items = []
        for item in self.__data['items'].values():
            itemInfo = Item(item).get_info()
            if itemInfo:
                self.Items.append(itemInfo)

class ProfileChange(Profile):
    def __init__(self, data):
        super(ProfileChange, self).__init__(data)

class LootResult():
    def __init__(self, lootResultInfo):
        self.lootResultInfo = lootResultInfo
        self.itemType = self.lootResultInfo['itemType']

    def get_info(self):
        return {
            'itemType': self.itemType
        }

class Purchases():
    def __init__(self, PurchasesInfo):
        self.PurchasesInfo = PurchasesInfo
        self.purchaseId = self.PurchasesInfo['purchaseId']
        self.purchaseDate = self.PurchasesInfo['purchaseDate']
        self.itemType = [LootResult(loot).get_info() for loot in self.PurchasesInfo['lootResult']]
        self.totalMtxPaid = self.PurchasesInfo['totalMtxPaid']

    def get_info(self):
        return {
            'purchaseId': self.purchaseId,
            'purchaseDate': self.purchaseDate,
            'itemType': self.itemType,
            'totalMtxPaid': self.totalMtxPaid
        }

class Purchases_history():
    def __init__(self, response):
        self.__data = response['profileChanges'][0]['profile']
        self.Stats = self.__data['stats']
        self.Attributes = self.Stats['attributes']
        self.mtx_purchase_history = [Purchases(purchas).get_info() for purchas in self.Attributes['mtx_purchase_history']['purchases']]

class Account():
    def __init__(self, AccountInfo):
        self.AccountInfo = AccountInfo
        self.displayName = self.AccountInfo['displayName']
        self.name = self.AccountInfo['name']
        self.email = self.AccountInfo['email']
        self.lastLogin = self.AccountInfo['lastLogin']
        self.country = self.AccountInfo['country']
        self.tfaEnabled = self.AccountInfo['tfaEnabled']