import requests
from ratelimit import limits, sleep_and_retry

MINUTE = 1

def getToken(BLIZZ_CLIENT,BLIZZ_SECRET):
    url='https://eu.battle.net/oauth/token?grant_type=client_credentials'
    myobj={'client_id': BLIZZ_CLIENT, 'client_secret': BLIZZ_SECRET}
    x=requests.post(url, data = myobj)
    if x.status_code == 200:
        return x.json()['access_token']
    else:
        print("Invalid credentials for the blizzard API")
        raise SystemExit(0)

def getRoster(token,realm,guild):
    anObj = {'access_token':token,'namespace':'profile-eu','locale':'en_US'}
    url = 'https://eu.api.blizzard.com/data/wow/guild/'+realm+'/'+guild+'/roster'
    y=requests.get(url,params=anObj)
    if y.status_code == 200:
        return y.json()['members']
    else:
        print("That guild/realm does not exist, check the spelling of them both")
        raise SystemExit(0)

@sleep_and_retry
@limits(calls=90,period=MINUTE)
def getProfessions(token,name,realm):
    anObj = {'access_token':token,'namespace':'profile-eu','locale':'en_US'}
    url = 'https://eu.api.blizzard.com/profile/wow/character/'+realm+'/'+name.lower()+'/professions'
    x=requests.get(url,params=anObj)
    if x.status_code==200:
        if 'primaries' in x.json():
            return x.json()['primaries']