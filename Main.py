print(
	"""
	PingPong 1.0.0
	Copyright (c) 2021 there-are-higher-beings
	Licensed under the GNU AGPL 3.0
	"""
)
#imports
import asyncio
import discord
import time
import random
from discord.ext import commands
from discord import utils
from discord.utils import get

#bunch of things to include to make the code run
intents = discord.Intents().all()  
client = commands.Bot(command_prefix = ["p]"], intents=intents)

#bunch of variables
pinger = [
	'hehe',
	'muahahahah',
	'suffer mortal',
	'sue me',
	'>:D'
]
ping_responses = [
	'stop',
	'stap',
	'please..',
	'really?',
	'can you not?',
	'bruh wth',
	'i will kick you',
	]

#message to send when running
@client.event
async def on_ready():
	print("Connected to Discord at " + time.ctime())
	perms = discord.Permissions(268438544)
	print("Invite link: {}".format(discord.utils.oauth_url(client.user.id, perms)))
		
	#what the bot is doing: playing 𝙋𝙞𝙣𝙜 𝙋𝙤𝙣𝙜
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="Ping Pong"))
	print('')
	print(':::')
	print('')

#a function to listen to sent messages
@client.listen('on_message')
async def msg(message):
	#ignores the msg if its sent by a bot, so that there isnt an infinite loop of messages (could be fun if its taken out tho tbh)
	if message.author == client.user:
		return
	
	#responding if the bot ever gets pinged (see variables)
	if client.user.mentioned_in(message):
		time.sleep(0.5)
		await message.channel.send(random.choice(ping_responses))
	
	#main ping function triggered with p[ping
	if message.content == 'p[ping':
		#change the 5 to however many minutes you want between ping cycles
		timeout = 60*5
		while True:
			guild = client.guilds[0]
			channel1 = random.choice(guild.text_channels)
			randomMember = random.choice(channel1.guild.members)
			message1 = await channel1.send(f'{randomMember.mention} ' + random.choice(pinger))
			await asyncio.sleep(2)
			await message1.delete()
			await asyncio.sleep(timeout)

#replace TOKEN with your token
client.run('TOKEN')
