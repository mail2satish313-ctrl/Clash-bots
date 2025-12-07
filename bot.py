import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Clash of Clans API configuration
COC_API_KEY = os.getenv('COC_API_KEY')
COC_API_BASE = 'https://api.clashofclans.com/v1'

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready to serve Clash of Clans data!')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    print(f'Message received: {message.content} from {message.author}')
    
    # Process commands
    await bot.process_commands(message)

@bot.command(name='ping', help='Test if bot is responding')
async def ping(ctx):
    """Simple test command"""
    await ctx.send('Pong! Bot is working!')

@bot.command(name='player', help='Get player info by tag. Usage: !player #TAG')
async def get_player(ctx, player_tag: str):
    """Fetch player information from Clash of Clans API"""
    if not player_tag.startswith('#'):
        await ctx.send('Player tag must start with #')
        return
    
    # Format tag for URL
    formatted_tag = player_tag.replace('#', '%23')
    
    headers = {
        'Authorization': f'Bearer {COC_API_KEY}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(f'{COC_API_BASE}/players/{formatted_tag}', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            embed = discord.Embed(
                title=f"{data['name']} ({data['tag']})",
                color=discord.Color.blue()
            )
            
            # Basic Info
            embed.add_field(name='🏛️ Town Hall', value=data['townHallLevel'], inline=True)
            embed.add_field(name='🏆 Trophies', value=f"{data['trophies']}/{data.get('bestTrophies', 'N/A')}", inline=True)
            embed.add_field(name='⭐ Level', value=data['expLevel'], inline=True)
            
            # War Stats
            embed.add_field(name='⚔️ War Stars', value=data.get('warStars', 0), inline=True)
            embed.add_field(name='🎯 Attack Wins', value=data.get('attackWins', 0), inline=True)
            embed.add_field(name='🛡️ Defense Wins', value=data.get('defenseWins', 0), inline=True)
            
            # League Info
            if 'league' in data:
                embed.add_field(name='🏅 League', value=data['league']['name'], inline=True)
            
            # War League
            if 'warLeague' in data:
                embed.add_field(name='🎖️ War League', value=data['warLeague']['name'], inline=True)
            
            # Builder Base
            if 'builderHallLevel' in data and data['builderHallLevel'] > 0:
                embed.add_field(name='🔨 Builder Hall', value=data['builderHallLevel'], inline=True)
                embed.add_field(name='🏆 Versus Trophies', value=f"{data.get('versusTrophies', 0)}/{data.get('bestVersusTrophies', 0)}", inline=True)
                embed.add_field(name='⚔️ Versus Wins', value=data.get('versusBattleWins', 0), inline=True)
            
            # Clan Info
            if 'clan' in data:
                clan_role = data.get('role', 'Member').capitalize()
                embed.add_field(name='🏰 Clan', value=f"{data['clan']['name']} ({clan_role})", inline=False)
            
            # Donations
            embed.add_field(name='🎁 Donations', value=data.get('donations', 0), inline=True)
            embed.add_field(name='📥 Received', value=data.get('donationsReceived', 0), inline=True)
            
            # Clan Capital
            if 'clanCapitalContributions' in data:
                embed.add_field(name='🏛️ Capital Gold', value=data['clanCapitalContributions'], inline=True)
            
            await ctx.send(embed=embed)
        elif response.status_code == 404:
            await ctx.send('Player not found!')
        else:
            await ctx.send(f'Error: {response.status_code}')
    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')

@bot.command(name='clan', help='Get clan info by tag. Usage: !clan #TAG')
async def get_clan(ctx, clan_tag: str):
    """Fetch clan information from Clash of Clans API"""
    if not clan_tag.startswith('#'):
        await ctx.send('Clan tag must start with #')
        return
    
    # Format tag for URL
    formatted_tag = clan_tag.replace('#', '%23')
    
    headers = {
        'Authorization': f'Bearer {COC_API_KEY}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(f'{COC_API_BASE}/clans/{formatted_tag}', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            embed = discord.Embed(
                title=f"{data['name']} ({data['tag']})",
                description=data.get('description', 'No description'),
                color=discord.Color.gold()
            )
            
            # Basic Stats
            embed.add_field(name='⭐ Clan Level', value=data['clanLevel'], inline=True)
            embed.add_field(name='👥 Members', value=f"{data['members']}/50", inline=True)
            embed.add_field(name='🏆 Clan Points', value=f"{data['clanPoints']:,}", inline=True)
            
            # Requirements
            embed.add_field(name='🎯 Required Trophies', value=f"{data['requiredTrophies']:,}", inline=True)
            embed.add_field(name='🏛️ Required TH', value=data.get('requiredTownhallLevel', 'Any'), inline=True)
            embed.add_field(name='🚪 Type', value=data.get('type', 'Unknown'), inline=True)
            
            # War Stats
            embed.add_field(name='⚔️ War Wins', value=data.get('warWins', 0), inline=True)
            embed.add_field(name='📊 War Win Streak', value=data.get('warWinStreak', 0), inline=True)
            embed.add_field(name='🔄 War Frequency', value=data.get('warFrequency', 'Unknown'), inline=True)
            
            # War League
            if 'warLeague' in data:
                embed.add_field(name='🎖️ War League', value=data['warLeague']['name'], inline=True)
            
            # War Win Rate
            war_wins = data.get('warWins', 0)
            war_losses = data.get('warLosses', 0)
            war_ties = data.get('warTies', 0)
            total_wars = war_wins + war_losses + war_ties
            if total_wars > 0:
                win_rate = (war_wins / total_wars) * 100
                embed.add_field(name='📈 War Win Rate', value=f"{win_rate:.1f}% ({war_wins}W-{war_losses}L-{war_ties}T)", inline=True)
            
            # Clan Capital
            if 'clanCapital' in data:
                embed.add_field(name='🏛️ Capital Hall', value=data['clanCapital'].get('capitalHallLevel', 'N/A'), inline=True)
            
            # Labels/Tags
            if 'labels' in data and data['labels']:
                labels_text = ', '.join([label['name'] for label in data['labels'][:3]])
                embed.add_field(name='🏷️ Labels', value=labels_text, inline=False)
            
            # Location
            if 'location' in data:
                location = f"{data['location'].get('name', 'Unknown')}"
                if 'isCountry' in data['location']:
                    location += f" {data['location'].get('countryCode', '')}"
                embed.add_field(name='🌍 Location', value=location, inline=True)
            
            await ctx.send(embed=embed)
        elif response.status_code == 404:
            await ctx.send('Clan not found!')
        else:
            await ctx.send(f'Error: {response.status_code}')
    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')

# Run the bot
if __name__ == '__main__':
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    if not DISCORD_TOKEN:
        print('Error: DISCORD_TOKEN not found in environment variables')
        print('Please set DISCORD_TOKEN in your cloud platform settings')
        exit(1)
    elif not COC_API_KEY:
        print('Error: COC_API_KEY not found in environment variables')
        print('Please set COC_API_KEY in your cloud platform settings')
        exit(1)
    else:
        print('Starting bot...')
        print(f'Discord Token: {"*" * 20}...{DISCORD_TOKEN[-10:]}')
        print(f'COC API Key: {"*" * 20}...{COC_API_KEY[-10:]}')
        try:
            bot.run(DISCORD_TOKEN)
        except Exception as e:
            print(f'Failed to start bot: {e}')
            exit(1)
