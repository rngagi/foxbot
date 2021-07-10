#!/usr/bin/env python3

import discord
from panbot_search import select_candidates
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
client = discord.Client()

help_text = ''' Welcome to **PANBot**!
To use the bot, type in /pan followed by your query:
> /pan dog

You can also search for multiple items at the same time:
> /pan sun moon

To search for a specific string instead of a list of words, use quotes:
> /pan "a dog"

You can also search PAn protoforms!
To do this, begin your query with an asterisk (*):
> /pan *num
Note that this does a partial search of all protoforms containing "num" (or "Num", it's not case sensitive!), not just protoforms that start with "num".

If your protoform query contains at least one uppercase character, it will become case sensitive. E.g.:
> /pan *Num
This will return all protoforms containing "Num", but not "num".

PMP search is also available!
Just start your query with /pmp
Just like PAn, you can use unquoted word lists, quoted strings, and protoforms with a preceding asterisk (*).

Have fun!
'''

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '/pan test':
        response = 'Panbot operational!'
        await message.channel.send(response)
        return

    if message.content.strip() in ['/pan help', '/pan ?']:
        await message.channel.send(help_text)
        return

    if message.content.startswith('/pan '):
        query = message.content.removeprefix('/pan ')
        response = select_candidates(query, 'pan')
        if len(response) > 10:
            await message.channel.send(
            'Too many results! Try specifying a narrower query.')
        else:
            for item in response:
                await message.channel.send(item)
            return

    if message.content.startswith('/pmp '):
        query = message.content.removeprefix('/pmp ')
        response = select_candidates(query, 'pmp')
        if len(response) > 10:
            await message.channel.send(
            'Too many results! Try specifying a narrower query.')
        else:
            for item in response:
                await message.channel.send(item)
            return

client.run(TOKEN)
