import requests, datetime, sys

languages = {
    'hu': 'Hungarian, Hungary',
    'nl': 'Dutch, Netherlands',
    'no': 'Norwegian, Norway',
    'pl': 'Polish, Poland',
    'pt-BR': 'Portuguese, Brazilian, Brazil',
    'ro': 'Romanian, Romania',
    'fi': 'Finnish, Finland',
    'sv-SE': 'Swedish, Sweden',
    'vi': 'Vietnamese, Vietnam',
    'tr': 'Turkish, Turkey',
    'cs': 'Czech, Czechia, Czech Republic',
    'el': 'Greek, Greece',
    'bg': 'Bulgarian, Bulgaria',
    'ru': 'Russian, Russia',
    'uk': 'Ukranian, Ukraine',
    'th': 'Thai, Thailand',
    'zh-CN': 'Chinese, China',
    'ja': 'Japanese',
    'zh-TW': 'Chinese, Taiwan',
    'ko': 'Korean, Korea'
}

locales = [
    "da", "de",
    "en-GB", "en-US",
    "es-ES", "fr",
    "hr", "it",
    "lt", "hu",
    "nl", "no",
    "pl", "pt-BR",
    "ro", "fi",
    "sv-SE", "vi",
    "tr", "cs",
    "el", "bg",
    "ru", "uk",
    "th", "zh-CN",
    "ja", "zh-TW",
    "ko"
]


def lookup(_token):
    headers = {
        'Authorization': _token,
        'Content-Type': 'application/json'
    }
    try:
        res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
        res = res.json()
        user_id = res['id']
        locale = res['locale']
        avatar_id = res['avatar']
        language = languages.get(locale)
        creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
            '%d-%m-%Y %H:%M:%S UTC')
    except KeyError:
        headers = {
            'Authorization': "Bot " + _token,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
            res = res.json()
            user_id = res['id']
            locale = res['locale']
            avatar_id = res['avatar']
            language = languages.get(locale)
            creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
                '%d-%m-%Y %H:%M:%S UTC')
            print(f"Name: `{res['username']}#{res['discriminator']} ` **BOT**\\nID: `{res['id']}`\\nEmail: `{res['email']}`\\nCreation Date: `{creation_date}`\\nFlags: {res['flags']}\\nLocal Language: {res['locale']}{language}\\nverified: {res['verified']}")
            print(f"avatar url: https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")
        except KeyError:
            print("Invalid token")
        print(f"Name: `{res['username']}#{res['discriminator']}`\\nID: `{res['id']}`\\nEmail: `{res['email']}`\\nCreation Date: `{creation_date}`")
    nitro_type = "None"
    if "premium_type" in res:
        if res['premium_type'] == 2:
            nitro_type = "Nitro Premium"
        elif res['premium_type'] == 1:
            nitro_type = "Nitro Classic"
    username = res["username"] + "#" + res['discriminator']
    print(f'user name: {username}')
    print(f"ID: " + res["id"])
    print(f'Phone: {res["phone"]}')
    print("Flags: " + str(res['flags']))
    print('Local language: ' + str(res['locale']) + f" - {language}")
    print('MFA: ' + str(res['mfa_enabled']))
    print('Verified: ' + str(res['verified']))
    print('Nitro: ' + str(nitro_type))
    print(f"avatar url: https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")

try:
    lookup(sys.argv[1])
except:
    lookup(input("token ->"))