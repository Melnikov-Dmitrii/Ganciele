from model_classes import Game, Player
import discord
from discord.ext import commands

games = {} #discordChannelID:game
players = {} #myID:discordID
dm_channels = {} #playerID:(discord_channelID, gameID)

with open("token.txt", "r") as f:
    token = f.read()
    
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} has connected to Discord!')

@bot.command()
async def start(ctx):
    game = Game()
    game.stage = 1
    games[ctx.channel.id] = game
    await ctx.send("Game#" + str(game.id) + " started. Type !join")


@bot.command()
async def end(ctx):
    game = games.get(ctx.channel.id)
    if game == None:
        return
    games.pop(ctx.channel.id)
    await ctx.message.add_reaction("👍")


@bot.command()
async def join(ctx):
    game = games.get(ctx.channel.id)
    if game == None:
        await ctx.send("There is not game here")
        return
    if game.stage != 1:    
        await ctx.send("The game is not recruiting players right now.")
        return
    for player in game.players:
        if players[player.id] == ctx.author.id:
            await ctx.send("You are already in this game")
            return
    player = Player()
    players[player.id] = ctx.author.id
    game.add_player(player)
    await ctx.message.add_reaction("👍")

@bot.command()
async def leave(ctx):
    game = games.get(ctx.channel.id)
    if game == None:
        await ctx.send("There is not game here")
        return
    if game.stage != 1:    
        await ctx.send("The game is not recruiting players right now.")
        return
    ID = 0
    for player in game.players:
        if players[player.id] == ctx.author.id:
            ID = player.id
    if ID == 0:
        await ctx.send("You wasn't in game")
        return
    game.remove_player(ID)
    players.pop(ID)
    await ctx.message.add_reaction("👍")

@bot.command()
async def list(ctx):
    game = games.get(ctx.channel.id)
    if game == None:
        await ctx.send("There is not game here")
        return
    res = "List of players:\n"
    for player in game.players:
        user = await bot.fetch_user(players[player.id])
        res = res + user.name + "\n"
    print(res)
    await ctx.send(res)


@bot.command()
async def begin(ctx):
    game = games.get(ctx.channel.id)
    if game == None:
        await ctx.send("There is not game here")
        return
    if game.stage != 1:    
        await ctx.send("The game is not recruiting players right now.")
        return
    game.stage = 2
    game.randomise_circle()
    for i in range(len(game.players)):
        ID = game.players[i].id
        user = await bot.fetch_user(players[ID])
        dm_channels[ID] = ((await user.create_dm()).id, ctx.channel.id)
        await user.send("You are creating a character for " + (await bot.fetch_user(players[game.players[i - 1].id])).name)
    await ctx.send("Time to create characters. Check your direct messages.")


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    channelID = message.channel.id
    playerID = 0
    game_channelID = 0
    for k, v in dm_channels.items():
        if v[0] == channelID:
            playerID = k
            game_channelID = v[1]
            break
    if playerID == 0:
        return

    game = games[game_channelID]
    game.set_secret_from_player(message.content, playerID)
    await message.add_reaction("👍")
    if game.check_secrets():
        game.stage = 3
        data = game.get_secrets_for_players()
        for data1 in data:
            mes = "Here are the characters of other players:\n"
            for s in data1[1]:
                mes += (await bot.fetch_user(players[s[0]])) + ": " + s[1] + "\n"
            await (await bot.fetch_user(players[data1[0]])).send(mes)
        await (await bot.fetch_channel(game_channelID)).send("All the characters were created. Have a nice game!")
        games.pop(game_channelID)
    
@bot.command()
async def check(ctx):
    print("games: ", games)
    print("players: ", players)
    print("dm_channels: ", dm_channels)
    
bot.run(token)
