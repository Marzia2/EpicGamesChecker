import time
import requests
from Model import *
def checker_fortnite(session: requests.Session, cookies:dict, check_fortnite:bool=False):
        for key, value in cookies.items():
            session.cookies.set(key, value)


        req = session.get('https://www.epicgames.com/id/api/redirect?clientId=3446cd72694c4a4485d81b77adbb2141&responseType=code', timeout=10)
        code = req.json()['authorizationCode']

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
        }
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'token_type': 'eg1'
        }
        session.headers.update(headers)
        response = session.post('https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token', data=data, timeout=10)
        print(response.text)
        eg1_token = response.json()['access_token']
        accountId = response.json()['account_id']
        session.headers.clear()


        headers = {
            'Authorization': f'bearer {eg1_token}',
            'Content-Type': 'application/json'
        }
        session.headers.update(headers)
        response = session.get(f'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{accountId}', timeout=10)
        accountInfo = Account(response.json())
        context = {
            'EpickAccountInfo':{
                'displayName': accountInfo.displayName,
                'accountName': accountInfo.name,
                'accountEmail': accountInfo.email,
                'accountLastLogin': accountInfo.lastLogin,
                'accountCountry': accountInfo.country,
                'accountTfaEnabled': accountInfo.tfaEnabled
            }
        }

        if check_fortnite:
            response_info = session.post(f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{accountId}/client/QueryProfile?profileId=athena&rvn=-1', json=data, timeout=10)
            response_purchases = session.post(f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{accountId}/client/QueryProfile', json=data, timeout=10)


            userProfileData = ProfileChange(response_info.json())

            userHistoryPurchases = Purchases_history(response_purchases.json())

            context['Fortnite'] = {
                'createdAt': userProfileData.created,
                'currentPassTier': userProfileData.Stats.Attributes.bookLevel,
                'lifetimeWins': userProfileData.Stats.Attributes.lifetimeWins,
                'currentLevel': userProfileData.Stats.Attributes.level,
                'accountLevel': userProfileData.Stats.Attributes.accountLevel,
                'oldSeasons': userProfileData.Stats.Attributes.past_seasons,
                'historyPurchases': userHistoryPurchases.mtx_purchase_history,
                'items': userProfileData.Items
            }
        return context


if __name__ == '__main__':
    session = requests.Session()
    st = time.time()
    result = checker_fortnite(session,{
        'EPIC_BEARER_TOKEN':''
    }, check_fortnite=True)
    fin = time.time()
    with open(f'response.json', 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, indent=4, ensure_ascii=False)