# gh-space-shooter 🚀

Transform your GitHub contribution graph into an epic space shooter game! 

![Example Game](example.gif)

## Features

- 🚀 **Galaga-style space shooter** - Classic arcade gameplay with your contribution data
- 📊 **GitHub integration** - Fetches your last 52 weeks of contributions automatically
- 🎮 **Smart enemy AI** - Multiple attack strategies (columns, rows, random patterns)
- 💥 **Particle effects** - Explosions with randomized particles and smooth animations
- 🎨 **Polished graphics** - Rounded enemies, smooth ship design, starfield background
- 📈 **Contribution stats** - View your coding activity statistics
- 💾 **Export options** - Save both the GIF and raw JSON data

## Installation

### From PyPI (Recommended)

```bash
pip install gh-space-shooter
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/gh-space-shooter.git
cd gh-space-shooter

# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Setup

1. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `read:user`
   - Copy the generated token

2. Set up your environment:
   ```bash
   # Copy the example env file
   touch .env
   echo "GH_TOKEN=your_token_here" >> .env
   ```

   Alternatively, export the token directly:
   ```bash
   export GH_TOKEN=your_token_here
   ```

## Usage

### Generate Your Game GIF

Transform your GitHub contributions into an epic space shooter!

```bash
# Basic usage - generates username-gh-space-shooter.gif
gh-space-shooter <username>

# Examples
gh-space-shooter torvalds
gh-space-shooter octocat

# Specify custom output filename
gh-space-shooter torvalds --output my-epic-game.gif
gh-space-shooter torvalds -o my-game.gif

# Choose enemy attack strategy
gh-space-shooter torvalds --strategy column   # Enemies attack in columns
gh-space-shooter torvalds --strategy row      # Enemies attack in rows
gh-space-shooter torvalds -s random           # Random chaos (default)
```

This creates an animated GIF showing:
- Your contribution graph as enemies (more contributions = stronger enemies)
- A Galaga-style spaceship battling through your coding history
- Enemy attack patterns based on your chosen strategy
- Smooth animations with randomized particle effects
- Your contribution stats displayed in the console

### Advanced Options

```bash
# Save raw contribution data to JSON
gh-space-shooter torvalds --raw-output data.json

# Load from previously saved JSON (saves API rate limits)
gh-space-shooter --raw-input data.json --output game.gif

# Combine options
gh-space-shooter torvalds -o game.gif -ro data.json -s column
```

### Data Format

When saved to JSON, the data includes:
```json
{
  "username": "torvalds",
  "total_contributions": 1234,
  "weeks": [
    {
      "days": [
        {
          "date": "2024-01-01",
          "count": 5,
          "level": 2
        }
      ]
    }
  ],
  "fetched_at": "2024-12-30T12:00:00"
}
```

## License

MIT
