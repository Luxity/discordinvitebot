'''
Automatically checks and roles members if they meet the criteria in `role_ranks`
Roles must be in the server and are case sensitive.
Adjust Role names and rank criteria as needed.
'''

import discord
client=discord.Client()


role_ranks={
	'Amber':range(5,9),
	'Sapphire':range(10,14),
	'Emerald':range(15,24),
	'Gold':range(25,49),
	'Crystal':range(50,99),
	'Diamond':range(100,100000)
}


@client.event
async def on_ready():
	global role_list
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	await client.change_presence(game=discord.Game(name='!invites - list your invites'))
	print('------\n')
	for server in client.servers:
		role_list=dict((role.name,role) for role in server.roles)

@client.event
async def on_member_join(new_member):
	invites=await client.invites_from(new_member.server)
	for member in new_member.server.members:
		if member.bot==False:
			uses=0
			prole=None
			for invite in invites:
				if invite.max_age==0 and invite.inviter==member:
					uses += invite.uses
			for role,used in role_ranks.items():
				if uses in used and role_list[role] not in member.roles:
					for mrole in member.roles:
						if mrole.name in role_ranks.keys():
							await client.remove_roles(member,mrole)
					await client.send_message(member,"Congratulations  {}, you have been promoted to **{}**!".format(member.mention,role))
					await client.add_roles(member,role_list[role])

@client.event
async def on_message(message):
	if message.content=='!invites':
		total_uses=0
		embed=discord.Embed(title='__Invites from {}__'.format(message.author.name))
		invites = await client.invites_from(message.server)
		for invite in invites:
			if invite.inviter == message.author and invite.max_age==0:
				total_uses += invite.uses
				embed.add_field(name='Invite',value=invite.id)
				embed.add_field(name='Uses',value=invite.uses)
				embed.add_field(name='Expires',value='Never')
		embed.add_field(name='__Total Uses__',value=total_uses)
		await client.send_message(message.channel,embed=embed)


bot.run("Mzk4OTMyODE1MTc5MTUzNDIw.DTGN3Q.axZmgo2Y65oCgB4Sg6bSGk-7zSE")
