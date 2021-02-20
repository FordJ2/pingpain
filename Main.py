print(
	"""
	PingPong 1.0.0
	Copyright (c) 2021 Jonathan Ford
	Licensed under the GNU AGPL 3.0
	"""
)
import asyncio
import discord
import time
import random
from discord.ext import commands
from discord import utils
from discord.utils import get
from keep_alive import keep_alive

intents = discord.Intents().all()  
#intents.members = True
client = commands.Bot(command_prefix = ["p]"], intents=intents)

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

@client.event
async def on_ready():
	print("Connected to Discord at " + time.ctime())
	perms = discord.Permissions(268438544)
	print("Invite link: {}".format(discord.utils.oauth_url(client.user.id, perms)))

	'''
	#Setting `Playing ` status
	await client.change_presence(activity=discord.Game(name="a game"))
	# Setting `Streaming ` status
	await client.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
	# Setting `Listening ` status
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
	# Setting `Watching ` status
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

	#base
	await client.change_presence(status=discord.Status.idle, activity=discord.watching("The Bee Movie"))
	'''

	await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="Ping Pong"))
	print('')
	print(':::')
	print('')

@client.listen('on_message')
async def msg(message):
	if message.author == client.user:
		return
	
	if client.user.mentioned_in(message):
		time.sleep(0.5)
		await message.channel.send(random.choice(ping_responses))

	if message.content == 'p[ping':
		timeout = 5
		while True:
			guild = client.guilds[0]
			channel1 = random.choice(guild.text_channels)
			randomMember = random.choice(channel1.guild.members)
			message1 = await channel1.send(f'{randomMember.mention} ' + random.choice(pinger))
			await asyncio.sleep(2)
			await message1.delete()
			await asyncio.sleep(timeout)

keep_alive()
client.run('TOKEN')
