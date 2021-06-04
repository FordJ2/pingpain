import asyncio
import discord
import time
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from keep_alive import keep_alive

intents = discord.Intents().all()
client = commands.Bot(command_prefix=["p]"], intents=intents)
client.remove_command('help')

pinger = ['hehe', 'muahahahah', 'suffer mortal', 'sue me', '>:D']
ping_responses = ['stop', 'stap', 'please..', 'really?', 'can you not?', 'bruh wth', 'i will kick you']
timeout = 60*60*1

check = {}
v = {}
c2 = []

@client.event
async def on_ready():
	print("Connected to Discord at " + time.ctime())
	perms = discord.Permissions(19456)
	print("Invite link: {}".format(discord.utils.oauth_url(client.user.id, perms)))

	await client.change_presence(status=discord.Status.online, activity=discord.Game(name="p]help"))
	print('Servers connected to:')
	for guild in client.guilds:
		print(guild.name)
	print('\n:::\n')

	while True:
		txt = open(f'c.txt', 'r')
		lines = txt.readlines()
		for line in lines:
			c2.append(line)
			await asyncio.sleep(0.2)
		txt.close()

@client.event
async def on_guild_join(guild):
	print(f"Joined: {guild.name}")

	while True:
		txt = open(f'c.txt', 'a')
		txt.write(f"\n{guild.name}")
		txt.close()

@client.command()
async def invite(ctx):
	perms = discord.Permissions(19456)
	await ctx.send(f'<{discord.utils.oauth_url(client.user.id, perms)}>')

@client.command()
@has_permissions(manage_guild=True)
async def verify(ctx):
	n = ctx.message.guild
	o = ctx.author

	try:
		x = v[n, o]
		await ctx.send(f'{o.mention} you are already verified')
	except:
		v[n, o] = n
		await ctx.send(f'{o.mention} you are now verified')

@client.command()
@has_permissions(manage_guild=True)
async def plink(ctx):
	m = ctx.channel.name
	n = ctx.message.guild
	o = ctx.author

	try:
		x = v[n, o]
	except:
		v[n, o] = n
		await ctx.send(f'{o.mention} you are verified')

	await asyncio.sleep(0.25)
	message = await ctx.send("Attack initiated.")
	await asyncio.sleep(2)
	await message.delete()
	await asyncio.sleep(2)

	check[m] = True
	while check[m] == True:
		randomMember = random.choice(ctx.channel.guild.members)
		message1 = await ctx.channel.send(f'{randomMember.mention} {random.choice(pinger)}')
		await asyncio.sleep(2)
		print(f"pinged {randomMember} in {n}")
		await message1.delete()
		await asyncio.sleep(timeout)

@client.command()
@has_permissions(manage_guild=True)
async def plonk(ctx):
	await asyncio.sleep(0.25)
	message = await ctx.send("Attack aborted.")
	await asyncio.sleep(2)
	await message.delete()
	await asyncio.sleep(2)

	m = ctx.channel.name
	check[m] = False

@client.command()
@commands.cooldown(1, 60*60*48, commands.BucketType.user)
async def troll(ctx, user : discord.Member = None):
	n = ctx.message.guild
	o = ctx.message.author

	if user is None:
		await ctx.send('Please provide a username')
	if user is not None:
		try:
			x = v[n, user]
			if x == n:
				await ctx.send(f'You cant do that! {user.mention} is verified')
				return
		except:
			await ctx.send('hehe')
			await user.send(f'get trolled nerd >:D\n*btw it was {o}*')
			await asyncio.sleep(1)
			txt = ['shrek', 'bee']
			file = random.choice(txt)
			txt = open(f'{file}.txt', 'r')
			lines = txt.readlines()
			for line in lines:
				await user.send(line)
				await asyncio.sleep(1)
			txt.close()

@troll.error
async def troll_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send('Someone else is being trolled, try again in `{e:.1f}` minutes'.format(e = error.retry_after/60))
	else:
		raise error

@verify.error
async def verify_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"lmao you don't have the permissions to do that smh")

@plink.error
async def plink_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"Stupid! {ctx.message.author.mention}, you don't have the permissions to enforce pain.")

@plonk.error
async def plonk_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"Dummy you cannot end your suffering.")

@client.command()
async def ping(ctx):
	ping_ = client.latency
	ping = round(ping_ * 1000)
	await ctx.send(f"> `my ping is {ping}ms`")

@client.group(invoke_without_command=True)
async def help(ctx):
	await asyncio.sleep(0.25)
	em = discord.Embed(title="Help Information", description="View help information for <@812489455498821697>", color=0x3670a2)
	em.set_thumbnail(url='https://cdn.discordapp.com/attachments/791892252544860180/840237065579921418/Screen_Shot_2021-05-07_at_10.40.22_AM.png')
	em.add_field(name="Plink", value="\nbegin the cycle\nof pinging\n> `p]plink`", inline=True)
	em.add_field(name="Plonk", value="\nstop the cycle\nof pinging\n> `p]plonk`", inline=True)
	em.add_field(name="Verify", value="\nsave yourself from\n*some* of the pain\n> `p]verify`", inline=True)
	em.add_field(name="Ping", value="\ncheck my\nresponse time\n> `p]ping`", inline=True)
	em.add_field(name="Troll", value="\ndo a bit of trolling ;]\n\n> `p]troll *user*`", inline=True)
	em.add_field(name="Invite", value="\ninvite the bot\nto your server\n> `p]invite`", inline=True)
	await ctx.send(embed=em)

@client.listen('on_message')
async def listen(message):
	m = message.guild.name
	n = message.guild
	o = message.author

	if o == client.user:
		return

	try:
		x = v[n, o]
		if x == n:
			return
	except:
		if client.user.mentioned_in(message):
			await message.author.send('you pinged me >:(')
			await message.channel.send(random.choice(ping_responses))
			txt = ['shrek', 'bee']
			file = random.choice(txt)
			txt = open(f'{file}.txt', 'r')
			lines = txt.readlines()
			for line in lines:
				await message.author.send(line)
				await asyncio.sleep(1)
			txt.close()
	
	txt1 = open('c.txt', 'r')
	txt2 = open('c.txt', 'a')
	lines = txt1.readlines()
	for line in lines:
		if line == m:
			
	txt1.close()
	txt2.close()

keep_alive()
client.run('TOKEN')
