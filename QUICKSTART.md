# Waks - Bitcoin Miner Web App

**Live Demo:** 🌍 Deploy now with one click below!

## Deploy to Heroku (FREE)

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ashermohamed546-arch/Waks)

## Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fashermohamed546-arch%2FWaks)

## Deploy to Render

```bash
# Go to https://render.com
# Click "New +"
# Select "Web Service"
# Connect your GitHub repo
# Select main branch
# Auto-detected as Python
# Click "Deploy"
```

## Quick Start Locally

```bash
# Clone
git clone https://github.com/ashermohamed546-arch/Waks.git
cd Waks

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python main.py --web --port 5000

# Visit http://localhost:5000
```

## Features

✅ Bitcoin Mining (CPU)
✅ BTC Calculator (24+ currencies)
✅ Mobile Money Transfer (MTN, Airtel, M-Pesa, etc.)
✅ Real-time Exchange Rates
✅ Profit Calculator
✅ Beautiful Web Dashboard

## What You Get

- 🏠 Home Page
- 📊 Dashboard (Real-time stats)
- 🧮 Calculator (BTC to all currencies)
- 📱 Mobile Money (Send to Africa)
- 💰 Wallet Manager
- 🔌 REST API

## Technology Stack

- **Backend:** Python Flask
- **Frontend:** Bootstrap 5
- **Database:** In-memory (expandable)
- **APIs:** CoinGecko (Exchange rates)
- **Deployment:** Heroku, Railway, Docker

## Usage Examples

### Web App
```
http://localhost:5000/
```

### API Examples
```bash
# Convert BTC to USD
curl "http://localhost:5000/api/calculator/convert?btc=0.1&currency=USD"

# Get providers
curl "http://localhost:5000/api/mobile-money/providers"

# Mining stats
curl "http://localhost:5000/api/mining/stats"
```

## Documentation

See [DEPLOY.md](DEPLOY.md) for deployment options and troubleshooting.

---

**Made with ❤️ for Bitcoin miners in Africa 🌍**
