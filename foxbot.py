#!/usr/bin/env python3

import discord
from foxbot_search import select_candidates
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN= os.environ["TOKEN"]
GUILD= os.environ["GUILD"]
# TOKEN = os.getenv('TOKEN')
# GUILD = os.getenv('GUILD')
client = discord.Client()

help_text = '''
for help:
> /fox help

for Seediq:
> /sdq 中文
'''

# ''' Welcome to **PANBot**!
# To use the bot, type in /pan followed by your query:
# > /pan dog
#
# You can also search for multiple items at the same time:
# > /pan sun moon
#
# To search for a specific string instead of a list of words, use quotes:
# > /pan "a dog"
#
# You can also search PAn protoforms!
# To do this, begin your query with an asterisk (*):
# > /pan *num
# Note that this does a partial search of all protoforms containing "num" (or "Num", it's not case sensitive!), not just protoforms that start with "num".
#
# If your protoform query contains at least one uppercase character, it will become case sensitive. E.g.:
# > /pan *Num
# This will return all protoforms containing "Num", but not "num".
#
# PMP search is also available!
# Just start your query with /pmp
# Just like PAn, you can use unquoted word lists, quoted strings, and protoforms with a preceding asterisk (*).
#
# Have fun!
# '''

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user:
        return

    if msg == '/fox test':
        response = 'Foxbot operational!'
        await message.channel.send(response)
        return

    if msg.strip() in ['/fox help', '/fox ?']:
        await message.channel.send(help_text)
        return

    if msg.startswith('/sdq '):
        lang = msg.split()[0][1:]
        query = msg[5:]
        response = select_candidates(query, lang)
        if len(response) > 15:
            await message.channel.send(
            f'Too many results ({len(response)})! Try specifying a narrower query.')
        else:
            await message.channel.send('\n'.join(response))
        return

client.run(TOKEN)
