async def handleMessage(bot, mid, author_id, message, message_object, thread_id, thread_type, **kwargs):
    try:
        _split = message.split(' ', 1) if message else ['']
        cmd, args = _split if len(_split) != 1 else [_split[0], '']
        
        # Vérifier si 'commands' existe avant d'y accéder
        if hasattr(bot, 'commands'):
            if cnp in bot.commands:
                function = bot.commands[cnp]
                is_need_prefix = function.get('usePrefix', True)
                is_admin_only = function.get('adminOnly', False)
                if bot.prefix != '' and is_need_prefix and not cmd.startswith(bot.prefix):
                    return await bot.sendMessage(text_formatter(":mono[This command requires the use of a prefix]"), thread_id, thread_type)
                elif is_admin_only and str(author_id) not in bot.admin:
                    return await bot.sendMessage(text_formatter(":mono[You don't have permission to use this command.]"), thread_id, thread_type)
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
                    return await function['def'](bot, message_data)
        else:
            raise AttributeError("The 'bot' object does not have 'commands'.")
    except AttributeError as err:
        bot.error(f"{err}", 'AttributeError')
    except bot.FBchatFacebookError as err:
        bot.error(f"{err}", 'FBchatFacebookError')
    except bot.FBchatException as err:
        bot.error(f"{err}", 'FBchatException')
    except Exception as err:
        bot.error(f"{err}", 'Exception')
