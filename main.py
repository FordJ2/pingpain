print("""
	pingPAIN 1.0.0
	Copyright (c) 2021 .wncry#4617
	Licensed under the GNU AGPL 3.0
	https://github.com/there-are-higher-beings/pingPAIN
	""")
import asyncio
import discord
import time
import random
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents().all()
client = commands.Bot(command_prefix=["p]"], intents=intents)
pinger = ['hehe', 'muahahahah', 'suffer mortal', 'sue me', '>:D']
ping_responses = ['stop', 'stap', 'please..', 'really?', 'can you not?', 'bruh wth', 'i will kick you']
timeout = 60*60*1

@client.event
async def on_ready():
	print("Connected to Discord at " + time.ctime())
	perms = discord.Permissions(268438544)
	print("Invite link: {}".format(discord.utils.oauth_url(client.user.id, perms)))
	await client.change_presence(status=discord.Status.online, activity=discord.Game(name="p[ping"))
	print('\n:::\n')

@client.command()
async def plink(ctx, arg):
	if arg == 'start':
		while True:
			randomMember = random.choice(ctx.channel.guild.members)
			message1 = await ctx.channel.send(f'{randomMember.mention} {random.choice(pinger)}')
			await asyncio.sleep(2)
			print(f"pinged {randomMember}")
			await message1.delete()
			await asyncio.sleep(timeout)

@client.listen('on_message')
async def msg(message):
	#msg = message.content.lower()
	if message.author == client.user:
		return
	if client.user.mentioned_in(message):
		await message.channel.send(random.choice(ping_responses))
		txt = ['shreck', 'bee']
		file = random.choice(txt)
		txt = open(f'{file}.txt', 'r')
		lines = txt.readlines()
		for line in lines:
			await message.author.send(line)
			await asyncio.sleep(1)
		txt.close()

client.run('TOKEN')
