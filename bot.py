import os
from dotenv import load_dotenv
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from time import sleep
import asyncio

from discord.ext import commands

URL = 'https://w2g.tv/'

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

opts = Options()
opts.headless = True
opts.add_argument("--mute-audio")
#opts.binary = firefox_binary
assert opts.headless
global browser
browser = Firefox(options = opts)
firefox_profile = FirefoxProfile()
firefox_profile.set_preference("media.volume_scale", "0.0")

current_room_url = ""

def create_room(yt_url):
  global browser
  browser = Firefox(options = opts, firefox_profile = firefox_profile)
  browser.maximize_window()
  browser.get(URL)
  try:
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[2]'))).click()
  except:
    print("Could not click cookie accept thingy.")

  try:
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, 'create_room_button'))).click()
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div'))).click()
    url_field = browser.find_element(By.ID, 'search-bar-input')
    url_field.send_keys(yt_url)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[4]/div[2]/form/div/button'))).click()
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/div/div[5]/div[4]/div/div[1]'))).click()
  except:
    print("Something broke :<")
  #/html/body/div[1]/div/div/div/div[2]/div/button[2]                     # Cookie  
  #/html/body/div[1]/div[2]/div[2]/div                                    # Join room button
  #/html/body/div[2]/div[1]/div[4]/div[2]/form/div/button                 # Search
  #/html/body/div[2]/div[2]/div[1]/div[1]/div/div[5]/div[4]/div/div[1]    # Element

  final_url = browser.current_url
  return final_url

bot = commands.Bot(command_prefix="$")

@bot.command()
async def w2g(ctx, arg):
  working_msg = await ctx.channel.send("working ...")

  room_url = create_room(arg)
  global current_room_url
  current_room_url = room_url
  room_msg = await ctx.channel.send(room_url)

  await asyncio.sleep(20)
  await ctx.message.delete()
  await working_msg.delete()
  await room_msg.delete()
  global browser
  os.system("pkill -f firefox-esr")
  browser.close()

@bot.command()
async def room(ctx):
  if current_room_url != "":
    await ctx.channel.send(current_room_url)
  else:
    await ctx.channel.send("no current room found. create one with: $w2g url")

@bot.command()
async def close(ctx):
  global browser
  browser.close()
  await ctx.channel.send("browser closed.")

@bot.command()
@commands.is_owner()
async def terminate(ctx):
  await ctx.channel.send("me ded.")
  quit()

bot.run(TOKEN)
