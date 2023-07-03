import discord
from discord import app_commands
from datetime import datetime
import random
import string

"""| START INITIALIZATION |"""
MY_GUILD = discord.Object(id=381609335291379725)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.all()
client = MyClient(intents=intents)

"""| ON READY |"""
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Managing applications'))
    print(f"Logged in as {client.user} (ID: {client.user.id})...")
    print("-----------")

    commands_role = client.get_guild(381609335291379725).get_role(828891908805492737)
    for member in commands_role.members:
        await member.remove_roles(commands_role)
    print(f"{commands_role.name} role removed from all members...")
    print("-----------")

    print("Questions counter initialized at 0...")
    print("-----------")

    print("Ready!")

"""| VOICE CHANNEL STATE UPDATE |"""
'''
@client.event
async def on_voice_state_update(member, before, after):
    commands_role = client.get_guild(381609335291379725).get_role(828891908805492737)
    audit_log = client.get_guild(381609335291379725).get_channel(859328948252442645)
    soundcloud_bot = client.get_guild(381609335291379725).get_member(890343617762304070)
    if not before.channel and after.channel and member != soundcloud_bot:
        await member.add_roles(commands_role)
        join_embed = discord.Embed(description = f":small_blue_diamond: {member.mention} **joined voice channel** `{after.channel.name}`", timestamp = datetime.now(), color = discord.Colour.green())
        join_embed.set_author(name = member.display_name, icon_url = member.display_avatar)
        await audit_log.send(embed = join_embed)
    elif before.channel and not after.channel and member != soundcloud_bot: 
        await member.remove_roles(commands_role)
        join_embed = discord.Embed(description = f":small_blue_diamond: {member.mention} **left voice channel** `{before.channel.name}`", timestamp = datetime.now(), color = discord.Colour.red())
        join_embed.set_author(name = member.display_name, icon_url = member.display_avatar)
        await audit_log.send(embed = join_embed)
'''

"""| EMBEDS DICTIONARY |"""
embed_dict = {}
global questions_counter
questions_counter = 0

"""| QUESTION COMMAND START |"""
@client.tree.command(name = "question", description = "Ask a question, anonymously or not!")
async def question(interaction : discord.Interaction):
    global questions_counter
    questions_counter += 1
    await interaction.response.send_modal(ExternalQuestionModal(questions_counter))


"""| QUESTION MODAL |"""
class QuestionModal(discord.ui.Modal, title = "Question"):
    question = discord.ui.TextInput(label = "Enter your question", style = discord.TextStyle.long, required = True)
    anonymous = discord.ui.TextInput(label = "Send this question anonymously?", style = discord.TextStyle.short, required = True, default = "Yes")
    # time length feature

class ExternalQuestionModal(QuestionModal):
    def __init__(self, id):
        super().__init__(timeout = None)
        self.primary_id = id

    async def on_submit(self, interaction: discord.Interaction):
        if self.anonymous.value.lower() in ["yes", "y", "ye"]:
            self.embed = discord.Embed(title = self.question, description = "", timestamp = datetime.now(), color = discord.Colour.teal()) 
            self.embed.set_author(name = "Anonymous", icon_url = client.user.avatar)
            self.embed.set_footer(text = "Do /question to submit a question")
        else:
            self.embed = discord.Embed(title = self.question, description = "", timestamp = datetime.now(), color = discord.Colour.teal())
            self.embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar)
            self.embed.set_footer(text = "Do /question to submit a question")
        
        embed_dict[self.primary_id] = self.embed

        await interaction.response.send_message(f"Question sent! ID:{self.primary_id}", ephemeral = True)
        await interaction.followup.send(embed = self.embed, view = ButtonView(self.embed, self.primary_id))

"""| ANSWER MODAL |"""
class AnswerModal(discord.ui.Modal, title = "Answer"):
    answer = discord.ui.TextInput(label = "Type your response here:", style = discord.TextStyle.long, required = True)
    anonymous = discord.ui.TextInput(label = "Send this response anonymously?", style = discord.TextStyle.short, required = True, default= "Yes")
    
class ExternalAnswerModal(AnswerModal):
    def __init__(self, id):
        super().__init__(timeout = None)
        self.primary_id = id
    
    async def on_submit(self, interaction: discord.Interaction):
        self.embed = embed_dict[self.primary_id]
        if self.anonymous.value.lower() in ["yes", "y", "ye"]:
            self.embed.add_field(name = "Anonymous", value = self.answer, inline = True)
        else:
            self.embed.add_field(name = interaction.user.display_name, value = self.answer, inline = True)
        await interaction.response.edit_message(embed = self.embed)

"""| COMMENT BUTTON |"""
class ButtonView(discord.ui.View):
    def __init__(self, embed, id):
        super().__init__(timeout = None)
        self.embed = embed
        self.primary_id = id
        self.respondents = []
    
    @discord.ui.button(label = "Share your thoughts", style = discord.ButtonStyle.blurple, custom_id = "join")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name in self.respondents:
            await interaction.response.send_message("*You already responded to that question you fucker*", ephemeral = True)
        else:
            self.respondents.append(interaction.user.display_name)
            await interaction.response.send_modal(ExternalAnswerModal(self.primary_id))

'''
"""| VERIFY COMMAND |"""
@client.tree.command(name = "verify", description = "Issue verification roles for new members")
async def verify(interaction : discord.Interaction, member: discord.Member):
    newest_role = client.get_guild(381609335291379725).get_role(385292167733706752) 
    unique_role = client.get_guild(381609335291379725).get_role(821142461366665257)
    common_role = client.get_guild(381609335291379725).get_role(821140191875039252)
    default_role = client.get_guild(381609335291379725).get_role(808598323396739073)
    games_role = client.get_guild(381609335291379725).get_role(821142807161995276)
    food_role = client.get_guild(381609335291379725).get_role(821576498536251404)
    about_role = client.get_guild(381609335291379725).get_role(821323880479195146)
    channels_role = client.get_guild(381609335291379725).get_role(823175809383923722)
    verified_role = client.get_guild(381609335291379725).get_role(829940668368945224) 
    roles = [newest_role, unique_role, common_role, default_role, games_role, food_role, about_role, channels_role, verified_role]

    if interaction.user.id != 259571192673861632:
        await interaction.response.send_message("You do not have permission to use this!", ephemeral = True)
    else:
        for role in roles:
            await member.add_roles(role)
        await interaction.response.send_message(f"{member.mention} has been verified!")  
'''

client.run("MTAzODI5NjY4NTI5MTUxMTkzMQ.Gl63Vb.TuRa1GodfqcRCp6Up1hF01R9dXQTxKAMCzzv0g")