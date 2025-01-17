# Facebot
A simple facebook bot made in python.

## example echo command
```python
# ./commands/echo.py

async def myFunction(bot, event):
  args = event.args
  if not args:
    return await event.sendReply("Please provide a message you want to echo.")
  return await bot.sendMessage(
    f"ECHO: {args}",
    event.thread_id,
    event.thread_type
  )

config = {
  "name": 'echo', # (required) your command name
  "def": myFunction, # (required) lagay mo dito yung function, pede rin 'function' ang key name
  "author": "Christopher", # (optional) Author name
  "usage": "{p}echo [text]", # command usage
  "description": "Text here...", # lagay mo dito description ng command,
  "usePrefix": False, # default False
  "adminOnly": False, # default False
}
```
```
