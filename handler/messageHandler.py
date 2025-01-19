from database import User
from util import text_formatter, getName

# Fonction pour obtenir le nom de l'utilisateur
async def get_name(fetchName, uid):
    try:
        Users = User()
        userX = Users.get(uid)
        if userX:
            if userX != 'Facebook User':
                return userX.get('name')
        else:
            nameX = getName(uid)
            if nameX != 'Facebook User':
                Users.add(uid, nameX)
                return nameX
            fetch = await fetchName(uid)
            tao = fetch.get(uid)
            name = tao.name
            Users.add(uid, name)
            return name
    except Exception as e:
        return "Facebook User"

# Classe qui contient les données d'un message
class MessageData:
    def __init__(self, **data):
        self.bot = data.get('client')
        self.cmd = data.get('cmd')
        self.args = data.get('args')
        self.mid = data.get('mid')
        self.author_id = data.get('author_id')
        self.message = data.get('message')
        self.message_object = data.get('message_object')
        self.thread_id = data.get('thread_id')
        self.thread_type = data.get('thread_type')
        self.reply = None
        self.line = "━━━━━━━━━━━━━━━━━━"
        self.font = text_formatter
        
        if self.message_object.replied_to:
            self.reply = self.message_object.replied_to

    # Méthode pour obtenir le nom de l'utilisateur
    async def getName(self, uid):
        name = await get_name(self.bot.fetchUserInfo, self.uid)
        return name

    # Méthode pour envoyer une réponse
    async def sendReply(self, message, auto_font=False, mentions=None):
        text = self.font(message) if auto_font else message
        return await self.bot.sendMessage(text, self.thread_id, self.thread_type, reply_to_id=self.mid, mentions=mentions)

# Classe Greeg qui gère le bot
class Greeg:
    def __init__(self):
        self.commands = {}  # Dictionnaire des commandes
        self.events = []  # Liste des événements (si nécessaire)
        self.prefix = "!"  # Préfixe pour les commandes
        self.admin = []  # Liste des administrateurs
        self.FBchatFacebookError = Exception  # Exception à gérer

    # Ajouter une commande au bot
    def add_command(self, cmd, func, use_prefix=True, admin_only=False):
        self.commands[cmd] = {
            'def': func,  # Fonction à exécuter pour la commande
            'usePrefix': use_prefix,  # Si la commande nécessite un préfixe
            'adminOnly': admin_only  # Si la commande est réservée aux admins
        }

    # Log des erreurs
    def error(self, message, error_type):
        print(f"[{error_type}] {message}")

    # Log des informations
    def logInfo(self, message, title=None):
        print(f"[INFO] {title if title else ''}: {message}")

    # Méthode pour envoyer un message
    async def sendMessage(self, message, thread_id, thread_type, reply_to_id=None, mentions=None):
        print(f"Message envoyé: {message}")
        # Implémentez ici la logique d'envoi du message

# Fonction pour gérer les messages et exécuter les commandes
async def handleMessage(bot, mid, author_id, message, message_object, thread_id, thread_type, **kwargs):
    try:
        _split = message.split(' ', 1) if message else ['']
        cmd, args = _split if len(_split) != 1 else [_split[0], '']
        
        cnp = cmd if bot.prefix == "" or not cmd.startswith(bot.prefix) else cmd[1:].lower()

        # Vérifier si la commande existe
        if cnp in bot.commands:
            function = bot.commands[cnp]
            is_need_prefix = function.get('usePrefix', True)
            is_admin_only = function.get('adminOnly', False)
            
            # Vérifier si la commande nécessite un préfixe
            if bot.prefix != '' and is_need_prefix and not cmd.startswith(bot.prefix):
                return await bot.sendMessage(":mono[Cette commande nécessite un préfixe]", thread_id, thread_type)
            # Vérifier si la commande est réservée aux admins
            elif is_admin_only and str(author_id) not in bot.admin:
                return await bot.sendMessage(":mono[Vous n'avez pas l'autorisation d'utiliser cette commande.]", thread_id, thread_type)
            else:
                sender = await get_name(bot.fetchUserInfo, author_id)
                message_data = MessageData(
                    cmd=cnp,
                    args=args,
                    mid=mid,
                    client=bot,
                    author_name=sender,
                    author_id=author_id,
                    message=message,
                    message_object=message_object,
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                mtg = f"[blue]ThreadID : [/blue] {thread_id}\n"
                mtg += f"[blue]Sender   : [/blue] {sender}\n"
                mtg += f"[blue]Command  : [/blue] [yellow]{cnp}[/yellow]"
                pnl = bot.logInfo(mtg, title=author_id)
                
                # Exécuter la fonction associée à la commande
                return await function['def'](bot, message_data)
        else:
            return await bot.sendMessage(":mono[Commande non trouvée.]", thread_id, thread_type)

    except AttributeError as err:
        bot.error(f"{err}", 'AttributeError')
    except bot.FBchatFacebookError as err:
        bot.error(f"{err}", 'FBchatFacebookError')
    except bot.FBchatException as err:
        bot.error(f"{err}", 'FBchatException')
    except Exception as err:
        bot.error(f"{err}", 'Exception')
    
