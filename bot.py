import discord
import os
import requests
import json
from discord.ext.commands import Bot
from discord.ext import commands
import discord

import praw
import re
from PIL import Image


bot = Bot("--")

from keep_alive import keep_alive


client = discord.Client()
bott = commands.Bot(command_prefix = '.')


def get_image():
  im = Image.open(requests.get("https://picsum.photos/200/300", stream=True).raw)
  return im

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
  print(f'{member} pool vantan neel ku. Avanum nasama poga poran.')

@client.event
async def on_member_remove(member):
  print(f'{member} kalambitan. Uruptruvano.')

@bott.command()
async def ping(ctx):
  await ctx.send('Pong!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

keep_alive()
client.run(os.getenv('TOKEN'))