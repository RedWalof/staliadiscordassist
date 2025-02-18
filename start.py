import os
from dotenv import load_dotenv
import discord
import asyncio
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from keep_alive import keep_alive

load_dotenv()

# Variables d'environnement et paramètres
TOKEN = os.getenv('Token_secret')
PREFIX = "!"
AUTHORIZED_SERVER_IDS = [1339640495231602711]
YOUTUBE_URL = 'https://www.youtube.com/watch?v=egPuGceJxg0'  # URL de la vidéo YouTube

# Intentions du bot
intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.members = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)
 
# Fonction de démarrage du bot
@client.event
async def on_ready():
    print(f'Bot connecté en tant que< {client.user.name}')
    for guild in client.guilds:
        print(f"Serveur connecté : {guild.name} (ID : {guild.id})")
    if not boucle.is_running():
        boucle.start()  # Démarre la boucle si elle n'est pas déjà en cours






# Fonction pour déconnecter le bot du canal vocal
async def leave():
    for vc in client.voice_clients:
        if vc.is_connected():
            await vc.disconnect()
            print(f"Déconnecté du salon vocal : {vc.channel.name}")
         

# Fonction pour se connecter à un salon vocal spécifique
async def connect_voice(guild_id: int, id_vocal: int):
    guild = discord.utils.get(client.guilds, id=guild_id)
    if guild:
        voice_channel = discord.utils.get(guild.voice_channels, id=id_vocal)
        voice_client = discord.utils.get(client.voice_clients, guild__id=guild_id)
        if voice_channel:
            if voice_client and voice_client.channel.id == id_vocal:
                return 'Bot déjà connecté au salon vocal'
                 # Vérifie si le joueur rejoint le salon spécifique
    if after.channel and after.channel.id == id_vocal:
        # Vérifie que le membre n'est pas celui à ignorer
        if member.id == 1310305003453550622:
            return

        # Récupérer le salon texte
        channel = client.get_channel(channel_id)
        if channel:
            try:
                await channel.send(f"⚠️ {member.mention} attend dans le salon **Attente Support** <@&{1340090330745278565}>.")
                print(f"Message envoyé dans {channel.name} ({channel.id}) pour {member.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du message : {e}")
        else:
            print(f"Erreur : Aucun salon texte trouvé avec l'ID {channel_id}.")
            else:
                await leave()
                vc = await voice_channel.connect()
                await asyncio.sleep(2)
                await play_youtube(vc)
                print(f"Connecté au salon vocal {voice_channel.name} sur le serveur {guild.name}.")
                    # Vérifie si le joueur rejoint le salon spécifique
    if after.channel and after.channel.id == id_vocal:
        # Vérifie que le membre n'est pas celui à ignorer
        if member.id == 1310305003453550622:
            return

        # Récupérer le salon texte
        channel = client.get_channel(channel_id)
        if channel:
            try:
                await channel.send(f"⚠️ {member.mention} attend dans le salon **Attente Support** <@&{1340090330745278565}>.")
                print(f"Message envoyé dans {channel.name} ({channel.id}) pour {member.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du message : {e}")
        else:
            print(f"Erreur : Aucun salon texte trouvé avec l'ID {channel_id}.")
        else:
            print(f"Salon vocal avec l'ID '{id_vocal}' introuvable.")
    else:
        print(f"Serveur avec l'ID '{guild_id}' introuvable.")

# Fonction pour lire une vidéo YouTube
async def play_youtube(vc):
    # Vérifier si le fichier audio existe avant de tenter de le jouer
    if os.path.exists('audio.mp3'):
        while vc.is_connected():  # Boucle tant que le bot reste connecté au salon vocal
            print("Lecture de l'audio...")
            vc.play(FFmpegPCMAudio('audio.mp3'), after=lambda e: print("Lecture terminée. Redémarrage..."))
            
            # Attendre que la lecture se termine avant de relancer
            while vc.is_playing():
                await asyncio.sleep(1)
            
            print("Redémarrage de la musique.")
            await asyncio.sleep(1)  # Petite pause avant de redémarrer pour éviter les conflits

    else:
        print("Erreur : le fichier audio n'a pas été trouvé après le téléchargement.")


async def check_vocal_connect(server_id, vocal_id):
    guild = client.get_guild(server_id)
    if not guild:
        return "Serveur introuvable."

    channel = guild.get_channel(vocal_id)
    if not channel or not isinstance(channel, discord.VoiceChannel):
        return "Salon vocal introuvable."

    voice_client = discord.utils.get(client.voice_clients, guild__id=server_id)
    if len(channel.members) == 0:
        return True
    else:
        if voice_client and voice_client.channel.id == vocal_id:
            if len(channel.members) == 1:
                return True
            else:
                return False
        else:
            return False

# Événement déclenché lorsqu'un utilisateur change d'état vocal
@client.event
async def on_voice_state_update(member, before, after):
    guild_id = 1339640495231602711  # ID du serveur
    id_vocal = 1340090222460801104  # ID du salon vocal
    channel_id = 1340396992035295242

    if before.channel is None and after.channel is not None:  # L'utilisateur a rejoint un salon vocal
        print(f"{member.name} a rejoint le salon vocal.")
        result = await check_vocal_connect(guild_id, id_vocal)
        if not result:
            await connect_voice(guild_id, id_vocal)
            await notify_support_channel(member, channel_id)
        else:
            await leave()

    elif before.channel is not None and after.channel is None:  # L'utilisateur a quitté un salon vocal
        print(f"{member.name} a quitté le salon vocal.")
        result = await check_vocal_connect(guild_id, id_vocal)
        if not result:
            await connect_voice(guild_id, id_vocal)
            await notify_support_channel(member, channel_id)
        else:
            await leave()

    elif before.channel != after.channel:  # L'utilisateur a changé de salon vocal
        print(f"{member.name} a changé de salon vocal.")
        result = await check_vocal_connect(guild_id, id_vocal)
        if not result:
            await connect_voice(guild_id, id_vocal)
            await notify_support_channel(member, channel_id)
        else:
            await leave()

# Boucle pour gérer les serveurs non autorisés
@tasks.loop(seconds=10)
async def boucle():
    for guild in client.guilds:
        if guild.id not in AUTHORIZED_SERVER_IDS:
            print(f"Serveur non autorisé : {guild.name}. Tentative de quitter...")
            try:
                await guild.leave()  # Quitte le serveur non autorisé
                print(f"Quitté le serveur : {guild.name}")
            except Exception as e:
                print(f"Erreur lors de la tentative de quitter le serveur : {e}")

# Lancer le bot
keep_alive()
client.run(TOKEN)
