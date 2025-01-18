import json
import asyncio
from rich.console import Console
from rich.panel import Panel

async def loadConfig(botName=None):
  data = {
    "prefix": None,
    "botName": botName,
    "owner": "Anonymous",
    "admin": [
      61571117768115
    ]
  }
  message = ""
  try:
    config = json.load(open('config.json', 'r'))
  except FileNotFoundError:
    print("\033[0;31m[CONFIG] \033[0mConfig file not found\n")
    return data
  await asyncio.sleep(0.2)
  prefix = config.get('prefix', '')
  if not isinstance(prefix, str):
    message += f"[red]PREFIX[/red] Invalid prefix data type\n"
    prefix = ''
  elif ' ' in list(prefix):
    prefix = ''
    message += f"[red]PREFIX[/red] Prefix must not include space\n"
  else:
    message += f"[blue]PREFIX[/blue] {prefix if prefix else 'No prefix'}\n"
  
  botName = config.get('botName', data['botName'])
  message += f"[blue]NAME[/blue] {botName}\n"
  owner = config.get("owner", data['owner'])
  message += f"[blue]OWNER[/blue] {owner}\n"
  _admin = config.get("admin", data['admin'])
  admin = [str(ad) for ad in _admin if isinstance(ad, int) or isinstance(ad, str)]
  message += f"[blue]ADMIN[/blue] {','.join(admin)}\n"
  
  panel = Panel(message[:-1], title="BOT CONFIG", border_style="royal_blue1")
  Console().print(panel)
  data['prefix'] = prefix
  data['botName'] = botName
  data['owner'] = owner
  data['admin'] = admin
  return data