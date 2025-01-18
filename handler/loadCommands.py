import os
import importlib
from rich.console import Console
from rich.panel import Panel

commands = {}

def loadCommands(_prefix):
  global commands
  if commands:
    return commands
  console = Console()
  files = list(filter(lambda file: file.endswith('.py') and file!='__init__.py',os.listdir('./commands')))
  message = ""
  for file in files:
    filepath = f"commands.{os.path.splitext(file)[0]}"
    module = importlib.import_module(filepath)
    config = getattr(module, 'config', None)
    if config:
      name = config.get('name')
      function = config.get('def')
      if config.get('function'):
        function = config.get('function')
        config['def'] = config.get('function')
        del config['function']
      if not name:
        message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Missing command name\n"
      elif not function:
        message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Missing command function\n"
      else:
        usePrefix = config.get('usePrefix', True)
        if not name.isalnum():
          message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Invalid command name\n"
        elif name.lower() in commands:
          message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Command '{name}' already exist\n"
        elif usePrefix not in [True, False]:
          message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Invalid usePrefix value\n"
        else:
          message += f"[blue]COMMAND[/blue] Loaded [yellow]{name.lower()}[/yellow] ({file})\n"
          admin_only = config.get('adminOnly', False)
          if not admin_only in [True,False]:
            admin_only = False
            message += f"╰─── Invalid usePrefix value\n"
          config['adminOnly'] = admin_only if admin_only in [True, False] else False
          
          config["usage"] = config.get("usage", "").replace('{p}', _prefix)
          config["description"] = config.get("description", 'No description.').replace('{p}', _prefix)
          commands[name.lower()] = config
  panel = Panel(message[:-1], title="COMMANDS", border_style='royal_blue1')
  console.print(panel)
  print()
  return commands