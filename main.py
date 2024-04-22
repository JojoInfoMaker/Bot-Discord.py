import discord
import ffmpeg
from discord.ext import commands
import requests

# Définissez vos intents
intents = discord.Intents.all()
intents.voice_states = True  # Si votre bot utilise des fonctionnalités vocale

# Configuration du bot Discord
bot = commands.Bot(command_prefix='!', intents=intents)

# Booléen pour suivre l'état de lecture
is_playing = False

# Fonction pour rejoindre un salon vocal
async def join_voice_channel(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        return await channel.connect()
    else:
        await ctx.send("Tu n'est pas connecter dans un Vocal, connecte-toi pour m'utiliser.")

# Commande pour jouer une vidéo YouTube
@bot.command()
async def play(ctx, *, url):
    global is_playing
    voice_channel = await join_voice_channel(ctx)
    audio_url = await get_audio_url(url)
    voice_channel.play(discord.FFmpegPCMAudio(audio_url))
    is_playing = True
    await ctx.send("Vidéo Lancer, bonne écoute 😉")

# Fonction pour obtenir l'URL audio à partir du serveur Node.js
async def get_audio_url(url):
    try:
        response = requests.get(f'http://localhost:3000/play?url={url}')
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f'Error fetching audio URL: {e}')
        return None

# Commande pour mettre en pause la lecture
@bot.command()
async def pause(ctx):
    global is_playing
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        is_playing = False
        await ctx.send("Vidéo Mise sur Pause.")

# Commande pour reprendre la lecture
@bot.command()
async def resume(ctx):
    global is_playing
    voice_client = ctx.voice_client
    if not voice_client.is_playing():
        voice_client.resume()
        is_playing = True
        await ctx.send("Vidéo Mise sur Play.")

# Commande pour déconnecter le bot du salon vocal
@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    await ctx.send("Merci de m'avoir utiliser :wave:")

# Gérer les interactions de bouton
@bot.event
async def on_component(interaction):
    global is_playing
    if interaction.custom_id == "pause":
        if is_playing:
            await interaction.send("Vidéo Mise sur Pause.")
            await pause(interaction)
    elif interaction.custom_id == "resume":
        if not is_playing:
            await interaction.send("Vidéo Mise sur Play.")
            await resume(interaction)

# Exécuter le bot
bot.run('VOTRE_TOKEN')
