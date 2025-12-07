# 🎮 Clash of Clans Discord Bot

A powerful Discord bot that fetches detailed Clash of Clans player and clan information using the official Clash of Clans API.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📊 **Detailed Player Stats** - View comprehensive player information including:
  - Town Hall level, trophies, and experience
  - War stars, attack wins, and defense wins
  - League and War League rankings
  - Builder Base statistics
  - Donation stats and Clan Capital contributions

- 🏰 **Clan Information** - Get full clan details:
  - Clan level, members, and points
  - War wins, losses, and win rate
  - War League tier
  - Clan Capital level
  - Location and labels

- 🚀 **Easy to Use** - Simple command interface with emoji-rich embeds

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!ping` | Test bot connection | `!ping` |
| `!player #TAG` | Get player statistics | `!player #2JU2Q9UGV` |
| `!clan #TAG` | Get clan information | `!clan #2PP` |

## 🛠️ Local Setup

### Prerequisites
- Python 3.11 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Clash of Clans API Key ([Get one here](https://developer.clashofclans.com))

### Installation

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/YOUR_USERNAME/clash-bots.git
   cd clash-bots
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```powershell
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your tokens
   ```

4. **Run the bot:**
   ```powershell
   python bot.py
   ```

## ☁️ Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:
- Railway (Recommended)
- Render
- Heroku
- Docker/Docker Compose

## 🔒 Security

- Never commit your `.env` file (already in `.gitignore`)
- Regenerate tokens if accidentally exposed
- Use environment variables in production
- Update COC API key IP restrictions when deploying to cloud

## 📝 Notes

- Player and clan tags must start with `#`
- Ensure bot has these Discord permissions:
  - Read Messages/View Channels
  - Send Messages
  - Embed Links
- COC API has IP restrictions - update when deploying to cloud

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

MIT License - feel free to use this bot for your own servers!

## 🆘 Support

Having issues? Check out:
- [Deployment Guide](DEPLOYMENT.md)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Clash of Clans API Docs](https://developer.clashofclans.com/)
