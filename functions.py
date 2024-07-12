import nextcord
def printingAllCommands(list: dict):
        command_list = ""
        index = 0
        for key, value in list.items():
            index +=1
            command_list += f"{index}. **{key}**: {value}\n"
        return command_list
        
def EmbedBuilder(title, description, color, name, icon_url, url:None):
    embed = nextcord.Embed(title=title, color=color, description=description, url=url)
    embed.set_author(name=name, icon_url=icon_url)
    embed.set_footer(text="All the best to you! Administrators")
    return embed