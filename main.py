import discord
from discord.ext import commands
import os
from fake_useragent import UserAgent
import requests
import sys
import re
import random
import praw
from keep_alive import keep_alive

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '.', intents = intents)


def get_valid_filename(s):
    ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^\w.]', '', s)[:200]


def erase_previous_line():
    # cursor up one line
    sys.stdout.write("\033[F")
    # clear to the end of the line
    sys.stdout.write("\033[K")

def get_pictures_from_subreddit(data, subreddit, location, nsfw):
    for i in range(len(data)):
        if data[i]['data']['over_18']:
            # if nsfw post and you only want sfw
            if nsfw == 'n':
                continue
        else:
            # if sfw post and you only want nsfw
            if nsfw == 'x':
                continue

        current_post = data[i]['data']
        image_url = current_post['url']
        if '.png' in image_url:
            extension = '.png'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url += '.jpeg'
            extension = '.jpeg'
        else:
            continue

        erase_previous_line()
        print('downloading pictures from r/' + subreddit +
              '.. ' + str((i*100)//len(data)) + '%')

        # redirects = False prevents thumbnails denoting removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if(image.status_code == 200):
            try:
                if os.path.exists(location + '' + get_valid_filename(current_post['title']) + extension):
                    return get_valid_filename(current_post['title']) + extension
                
                else: 
                    output_filehandle = open(
                    location + '' + get_valid_filename(current_post['title']) + extension, mode='bx')
                    output_filehandle.write(image.content)
                    return get_valid_filename(current_post['title']) + extension
            except:
                pass
        

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
    channel = client.get_channel(806975695695380510)
    await channel.send(f'{member} Vantiya neel ku. Ivanum nasama poga poran.')
  

@client.command()
async def ping(ctx):
  await ctx.send(f'{round(client.latency * 1000)} ms')


@client.command()
async def pic(ctx):
  await ctx.send(file=discord.File('my_image.jpg'))

@client.command()
async def r(ctx, sub):
  ua = UserAgent(fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')
  num = random.randint(0,20)
  url = 'https://www.reddit.com/r/' + sub + '/top/.json?sort=top&t=all&limit=20'
  after = ''
  print(num)
  for i in range(0, 20):
      
      
         
        if after != None:
            print(after)
            url = url + '&after=' + after
        response = requests.get(url, headers={'User-agent': ua.random})
    
        after = response.json()['data']['after']

        location = os.path.join('', 'itookapicture')
        data = response.json()['data']['children']
        erase_previous_line()
        
        if(i==num):
            pic = get_pictures_from_subreddit(data, sub, '', 'y')
            erase_previous_line()
            print('Downloaded pictures from r/')
            print(pic)
            await ctx.send(file=discord.File(pic))
            os.remove(pic)

@client.command() 
async def meme(ctx):
    reddit = praw.Reddit(client_id='',
                        client_secret='	',
                        user_agent='')

    submission = reddit.subreddit("memes").random()
    await ctx.send(submission.url)

@client.command()
async def clear(ctx, number):
    num = int(number)
    await ctx.channel.purge(limit=num)

def delete_stuff():
    print(os.getcwd())
    dir_name = "/home/runner/BigPP69"
    test=os.listdir("/home/runner/BigPP69")
    for item in test:
        if item.endswith(".jpeg"):
            print (item)
            os.remove(os.path.join(dir_name, item))
            
keep_alive()
client.run(os.getenv('TOKEN'))