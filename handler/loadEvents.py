import os
import importlib
from rich.console import Console
from rich.panel import Panel

events = []

def loadEvents():
  global events
  if events:
    return events
  console = Console()
  files = list(filter(lambda file: file.endswith('.py') and
  file!='__init__.py',os.listdir('./events')))
  message = ""
  for file in files:
    filepath = f"events.{os.path.splitext(file)[0]}"
    module = importlib.import_module(filepath)
    config = getattr(module, 'config', None)
    if config:
      event_type = config.get('event')
      function = config.get('def')
      if not event_type:
        message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Missing event type\n"
      elif not function:
        message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Missing event function\n"
      else:
        if not event_type.startswith('type:'):
          message += f"[bold red]ERROR[/bold red] [red]{file} [white]- Missing event function\n"
        else:
          config["event"] = config["event"].lower()
          events.append(config)
          message += f"[blue]EVENT[/blue] Loaded [yellow]{file}[/yellow]\n"
  panel = Panel(message[:-1], title="EVENTS", border_style="royal_blue1")
  console.print(panel)
  print()
  return events