# W2DISC - A small discord bot for managing Watch2Gether (non-official)

This utility aims to provide simple access to the Watch2Gether service using a discord bot.
It is mainly used to quickly generate a room from a given YouTube URL by using the official Watch2Gether API (see [the API documentation](https://community.w2g.tv/t/watch2gether-api-documentation/133767) for more info).
Feel free to fork and add your own commands & functionality.

## Usage:

Install on the server of your choice or run locally on your computer.
In order to use the bot you have to import your own discord api key and Watch2Gether api key and put them into an environment file called `.env` using the following notation:

```
DISCORD_TOKEN = YOUR_TOKEN_HERE
W2G_API_KEY = YOUR_TOKEN_HERE
```

## User Commands:

```
$w2g [URL]      # create a new room with the specified URL
$room           # return the current room URL
$add [URL]      # add the URL to the playlist of the current room
```

## Admin Commands:

```
$stats          # display the number of created rooms
$terminate      # kill the bot on the server it's running on
```
