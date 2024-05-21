import discord
import requests

from requests.cookies import RequestsCookieJar
from discord.ext import commands
from discord import app_commands

# Define the intents
intents = discord.Intents.default()
intents.message_content = True

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to interact with the AI API
def AI(query: str) -> str:
    prompt = " Tu es une IA de 16 ans, décontractée, qui sait expliquer simplement les choses quand on lui demande, sinon tu dois répondre naturellement comme un enfant de 16 ans."
    query = query + prompt + " Uniquement des réponses courtes. Ne fais pas de commentaire. N'écris pas de code."
    url = "https://www.phorm.ai/api/db/generate_answer"
    headers = {
        "authority": "www.phorm.ai",
        "method": "POST",
        "path": "/api/db/generate_answer",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5",
        "origin": "https://www.phorm.ai",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Content-Type": "application/json"
    }

    session = requests.Session()
    session.headers.update(headers)

    payload = {
        "query": query,
        "project": "7bd6a01d-bad3-473d-b9b6-fd634fb6a4f6",
        "repos": ["https://github.com/xenocoderce/philosofiche/tree/main"]
    }

    response = session.post(url, json=payload)
    response.raise_for_status()
    return response.json()['answer']

# Define a slash command
@bot.tree.command(name='ping', description='Replies with Pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')
    
# Define a slash command for the bot to interact with the AI
@bot.tree.command(name='ask', description='Pose une question à Socrate')
@app_commands.describe(query='La question à poser à Socrate')
async def ask_ai(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    try:
        print("Proposition à l'I.A. : " + query)
        answer = AI(query)
        print("Réponse : " + answer)
        await interaction.followup.send(f'{answer}')
    except Exception as e:
        await interaction.followup.send("🤯 Franchement j'sais pas quoi répondre !")


# Event listener for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    # Sync the commands with Discord.
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

# Run the bot
bot.run('')
