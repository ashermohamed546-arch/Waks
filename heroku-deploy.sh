#!/bin/bash
# Heroku deployment script
# Run this to deploy to Heroku

echo "====================================="
echo "Waks - Bitcoin Miner"
echo "Heroku Deployment Script"
echo "====================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Check if Heroku is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI not found!"
    echo "Download it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "Logging into Heroku..."
heroku login

echo ""
read -p "Enter app name (e.g., waks-bitcoin-miner-yourname): " app_name

echo ""
echo "Creating Heroku app: $app_name"
heroku create $app_name

echo ""
echo "Setting environment variables..."
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))') --app $app_name
heroku config:set FLASK_ENV=production --app $app_name
heroku config:set FLASK_DEBUG=False --app $app_name

echo ""
echo "Deploying to Heroku..."
git push heroku main

echo ""
echo "====================================="
echo "Deployment Complete!"
echo "====================================="
echo ""
echo "Your app is live at:"
echo "https://$app_name.herokuapp.com"
echo ""
echo "Open it now:"
heroku open --app $app_name
