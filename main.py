import asyncio
import discord
import json
import random
from datetime import date
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	try:
		return prefixes[str(message.guild.id)]
	except:
		pass

def immunization_check(server, user):
	with open('immunized.json', 'r') as e:
		immunized = json.load(e)
	if (f'{str(server)} {str(user)}') in immunized:
		return True
	else:
		return False


def prefix(server):
	with open('prefixes.json', 'r') as f:
		prefix = json.load(f)

	try:
		return prefix[str(server)]
	except:
		pass

def immunization_inator(server, user):
	today = date.today()
	with open('immunized.json', 'r') as e:
		immunized = json.load(e)
	immunized[f'{str(server)} {str(user)}'] = today.strftime("%b-%d-%Y")
	with open('immunized.json', 'w') as e:
		json.dump(immunized, e, indent=4)


intents = discord.Intents().all()
client = commands.Bot(command_prefix = get_prefix, intents=intents)
client.remove_command('help')

#basic var
pinger = ['hehe', 'muahahahah', 'suffer mortal', 'sue me', '>:D', 'lol gottem', 'kekw', 'lmao']
timeout = 60*60*1

#lists/dictionaries
check = {}

@client.event
async def on_ready():
	perms = discord.Permissions(268438600)
	print('''
	Logged in as
	Username:  {0}
	User ID: {1}
	'''.format(client.user.name, client.user.id))

	print('\tServers connected to:')
	for guild in client.guilds:
		print("\t\t- {}".format(guild.name))

	print("\n---------------------------------\n{}\n---------------------------------".format(discord.utils.oauth_url(client.user.id, perms)))

	await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="the world burn"))
	
	print('\n:::\n')

@client.event
async def on_guild_join(guild):
	print(f"Joined: {guild.name}")
	
	#add prefix to json
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	prefixes[str(guild.id)] = 'p]'
	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

	#add server to json
	with open('servers.json', 'r') as e:
		servers = json.load(e)
	servers[str(guild.name)] = str(guild.id)
	with open('servers.json', 'w') as e:
		json.dump(servers, e, indent=4)

@client.event
async def on_guild_remove(guild):
	print(f"Left: {guild.name}")

	#remove prefix from json
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	prefixes.pop(str(guild.id))
	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

	#remove server from json
	with open('servers.json', 'r') as e:
		servers = json.load(e)
	servers.pop(str(guild.name))
	with open('servers.json', 'w') as e:
		json.dump(servers, e, indent=4)

@client.command()
@has_permissions(manage_guild=True)
async def changeprefix(ctx, prefix):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	prefixes[str(ctx.guild.id)] = prefix
	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

	await ctx.send(f'> Prefix changed to: `{prefix}`')

@client.command()
@has_permissions(manage_guild=True)
async def immunize(ctx, user : discord.Member = None):
	n = ctx.guild
	o = ctx.author

	if user is None:
		if immunization_check(n.name, o) == True:
			await ctx.reply('You are already immune')
		elif immunization_check(n.name, o) == False:
			immunization_inator(n.name, o)
			await ctx.reply('You are now immune')

	elif user is not None:
		if immunization_check(n.name, user) == True:
			await ctx.reply(f'{user.mention} is already immune')
		elif immunization_check(n.name, user) == False:
			immunization_inator(n.name, user)
			await ctx.reply(f'{user.mention} is now immune')


	else:
		print('if error 1')

@client.command()
async def invite(ctx):
	perms = discord.Permissions(19456)
	await ctx.send(f'<{discord.utils.oauth_url(client.user.id, perms)}>')

@client.command()
@has_permissions(manage_guild=True)
async def plink(ctx):
	m = ctx.channel.name
	n = ctx.message.guild
	o = ctx.author

	# adds person to immunized list
	if immunization_check(n.name, o) == True:
		pass
	elif immunization_check(n.name, o) == False:
		immunization_inator(n.name, o)
		message0 = await ctx.reply('You are now immune')
		
		await asyncio.sleep(2)
		await message0.delete()

	await asyncio.sleep(0.25)
	message = await ctx.send("Attack initiated.")
	await asyncio.sleep(2)
	await message.delete()
	await asyncio.sleep(2)

	#pings random member
	check[m] = True
	while check[m] == True:
		randomMember = random.choice(ctx.channel.guild.members)
		message1 = await ctx.send(f'{randomMember.mention} {random.choice(pinger)}')
		await asyncio.sleep(2)
		print(f"pinged {randomMember} in {n}")
		await message1.delete()
		await asyncio.sleep(timeout)

#stops the pinging
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

#madlad moment
@client.command()
@commands.cooldown(1, 60*60*4, commands.BucketType.user)
async def troll(ctx, user : discord.Member = None):
	n = ctx.message.guild
	o = ctx.message.author

	if user is None:
		await ctx.send('Please provide a username')
	if user is not None:
	
		if immunization_check(n.name, user) == True:
			await ctx.send(f'You cant do that! {user.mention} is immune')
			return
		elif immunization_check(n.name, user) == False:
			await ctx.send('hehe')
			await user.send(f'get trolled nerd >:D\n*btw it was {o}*')
			await asyncio.sleep(1)
			txt = ['shrek', 'bee', 'minc']
			file = random.choice(txt)
			txt = open(f'{file}.txt', 'r')
			lines = txt.readlines()
			for line in lines:
				await user.send(line)
				await asyncio.sleep(1)
			txt.close()

@client.command()
async def ping(ctx):
	ping_ = client.latency
	ping = round(ping_ * 1000)
	await ctx.send(f"> `{ping}ms`")

@client.group(invoke_without_command=True)
async def help(ctx):
	n = ctx.guild.id
	await asyncio.sleep(0.25)
	file = discord.File("pfp.png")
	em = discord.Embed(title="Help Information", description="View help information for <@875918645694435359>", color=0x3670a2)
	em.set_thumbnail(url='attachment://pfp.png')
	em.add_field(name="Plink", value=f"\nBegin the pain\n> `{prefix(n)}plink`", inline=True)
	em.add_field(name="Plonk", value=f"\nStop the pain\n> `{prefix(n)}plonk`", inline=True)
	em.add_field(name="Troll", value=f"\nDo a bit of trolling ;]\n> `{prefix(n)}troll *user*`", inline=True)
	em.add_field(name="Invite", value=f"\nInvite the bot to\nanother server\n> `{prefix(n)}invite`", inline=True)
	em.add_field(name="Immunize", value=f"\nSave yourself from\n*some* of the pain\n> `{prefix(n)}immunize`", inline=True)
	em.add_field(name="Change Prefix", value=f"\nChange the bot's\nprefix in your server\n> `{prefix(n)}changeprefix`", inline=True)
	await ctx.send(file=file, embed=em)

#on message
@client.listen('on_message')
async def listen(message):
	if message.author == client.user:
		return

	if client.user.mentioned_in(message):
		await message.channel.send('> My prefix here is: `{0}`\n> Try `{0}help` for more info.'.format(prefix(message.guild.id)))



#error messages
@changeprefix.error
async def changeprefix_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.reply(f"Lmao! You don't have the permissions to change the prefix.")
@troll.error
async def troll_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.reply('Someone else is being trolled, try again in `{e:.1f}` minutes'.format(e = error.retry_after/60))
	else:
		raise error
@immunize.error
async def immunize_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.reply(f"Lmao you don't have the permissions to do that smh")
@plink.error
async def plink_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.reply(f"Stupid! You don't have the permissions to enforce pain.")
@plonk.error
async def plonk_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.reply(f"Dummy, you cannot end your suffering.")

client.run('TOKEN')
