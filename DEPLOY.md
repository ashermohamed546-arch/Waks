# Deployment Guide - Waks Bitcoin Miner

## Quick Deploy Options

### Option 1: Heroku (FREE - 5000 dyno hours/month)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create waks-bitcoin-miner

# Deploy from Git
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

**Your app will be live at:** `https://waks-bitcoin-miner.herokuapp.com`

### Option 2: Railway.app (FREE tier available)

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account
5. Select `ashermohamed546-arch/Waks` repository
6. Click "Deploy"

**Railway will automatically detect Flask and deploy!**

### Option 3: Replit (FREE - instant deployment)

1. Go to https://replit.com
2. Click "Import from GitHub"
3. Paste: `https://github.com/ashermohamed546-arch/Waks`
4. Click "Import"
5. Click "Run"

**Your app will be live in seconds!**

### Option 4: PythonAnywhere (FREE with domain)

1. Go to https://www.pythonanywhere.com
2. Click "Start exploring PythonAnywhere"
3. Sign up (free account)
4. Create new web app
5. Choose Flask
6. Upload files via Git
7. Click "Reload"

### Option 5: Docker + Any Cloud (AWS, GCP, Azure, DigitalOcean)

#### Build Docker Image

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-c", "from web.app import create_app; import json; config = json.load(open('config.json')); app = create_app(config); app.run(host='0.0.0.0', port=5000)"]
EOF

# Build image
docker build -t waks-bitcoin-miner .

# Run locally first
docker run -p 5000:5000 waks-bitcoin-miner
```

#### Deploy to DigitalOcean (easiest)

1. Create DigitalOcean account
2. Create App Platform project
3. Connect GitHub repository
4. Select `Waks` repo
5. Click "Deploy"

---

## RECOMMENDED: Deploy to Heroku NOW (5 minutes)

```bash
# 1. Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Create Procfile
echo "web: python -c 'from web.app import create_app; import json; config = json.load(open(\"config.json\")); app = create_app(config); app.run(host=\"0.0.0.0\", port=int(os.environ.get(\"PORT\", 5000)))' " > Procfile

# 4. Create runtime.txt
echo "python-3.9.16" > runtime.txt

# 5. Push to Heroku
heroku create waks-bitcoin-miner-YOURNAME
git push heroku main

# 6. Open in browser
heroku open
```

**DONE! Your app is live!** 🚀

---

## Environment Variables

Add these to your hosting platform:

```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## Access Your Live App

After deployment:

- **Home:** https://your-app-name.herokuapp.com/
- **Dashboard:** https://your-app-name.herokuapp.com/dashboard
- **Calculator:** https://your-app-name.herokuapp.com/calculator
- **Mobile Money:** https://your-app-name.herokuapp.com/mobile-money
- **API Health:** https://your-app-name.herokuapp.com/api/health

---

## Troubleshooting

**App won't start?**
```bash
heroku logs --tail
```

**Need to update code?**
```bash
git push heroku main
heroku restart
```

**Want custom domain?**
```bash
heroku domains:add yourdomain.com
```

---

## Next Steps

1. �� Deploy (choose option above)
2. ✅ Share your link
3. ✅ Start mining
4. ✅ Use calculator
5. ✅ Send mobile money

Your Bitcoin miner is now **LIVE on the internet!** 🌍
