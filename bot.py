import os
from typing import Any
from dotenv import load_dotenv
import requests
import json
from time import sleep
import asyncio

from discord.ext import commands

# API documentation: https://community.w2g.tv/t/watch2gether-api-documentation/133767
BASE_URL = "https://api.w2g.tv"
W2G_URL = f"{BASE_URL}/rooms/create.json"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
W2G_API_KEY = os.getenv("W2G_API_KEY")

CURRENT_ROOM_KEY = ""
ROOMS_CREATED = 0

W2G_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def make_url_string():
    return f"{BASE_URL}/rooms/{CURRENT_ROOM_KEY}"


def create_room(yt_url):
    post_req = {
        "w2g_api_key": W2G_API_KEY,
        "share": yt_url,
        "bg_color": "#2d3c4a",
        "bg_opacity": "50",
    }
    json_post = json.dumps(post_req, indent=4)
    res = requests.post(W2G_URL, data=json_post, headers=W2G_HEADERS)
    json_res = json.loads(res.content)
    stream_key = json_res["streamkey"]
    global CURRENT_ROOM_KEY
    CURRENT_ROOM_KEY = stream_key
    global ROOMS_CREATED
    ROOMS_CREATED = +1
    return make_url_string()


def add_to_playlist(yt_url):
    post_req = {"w2g_api_key": W2G_API_KEY, "add_items": [{"url": yt_url}]}
    json_post = json.dumps(post_req, indent=4)
    res = requests.post(
        f"{BASE_URL}/rooms/{CURRENT_ROOM_KEY}/playlists/current/playlist_items/sync_update",
        data=json_post,
        headers=W2G_HEADERS,
    )
    if res.status_code == 200:
        return "Added successfully!"
    else:
        return "Could not add to playlist ..."


def get_room():
    return CURRENT_ROOM_KEY


bot = commands.Bot(command_prefix="$")


@bot.command()
async def w2g(ctx, arg):

    room_url = create_room(arg)
    room_msg = await ctx.channel.send(room_url)

    await ctx.message.delete()
    await asyncio.sleep(120)
    await room_msg.delete()


@bot.command()
async def room(ctx):
    room_msg: Any
    if CURRENT_ROOM_KEY != "":
        room_msg = await ctx.channel.send(make_url_string())
    else:
        room_msg = await ctx.channel.send(
            "no current room found. create one with: $w2g url"
        )

    await ctx.message.delete()
    ctx.message.user
    await asyncio.sleep(120)
    await room_msg.delete()


@bot.command()
async def add(ctx, arg):
    room_msg = Any
    if CURRENT_ROOM_KEY == "":
        room_msg = await ctx.channel.send(
            "no current room found. create one with: $w2g url"
        )
    else:
        result = add_to_playlist(arg)
        room_msg = await ctx.channel.send(result)

    await ctx.message.delete()
    await asyncio.sleep(20)
    await room_msg.delete()


@bot.command()
@commands.is_owner()
async def terminate(ctx):
    room_msg = await ctx.channel.send("terminating bot.")

    await asyncio.sleep(20)
    await ctx.message.delete()
    await room_msg.delete()
    quit()


@bot.command()
@commands.is_owner()
async def stats(ctx):
    room_msg = await ctx.channel.send(f"Total rooms created: {ROOMS_CREATED}")

    await asyncio.sleep(20)
    await ctx.message.delete()
    await room_msg.delete()


bot.run(TOKEN)
