#!/bin/bash
# Quick deployment script

echo "====================================="
echo "Waks - Bitcoin Miner Deployment"
echo "====================================="
echo ""

echo "Choose deployment option:"
echo "1) Heroku (FREE)"
echo "2) Railway.app (FREE)"
echo "3) Replit (FREE)"
echo "4) Docker Build"
echo ""
read -p "Enter option (1-4): " option

case $option in
  1)
    echo ""
    echo "Deploying to Heroku..."
    echo ""
    echo "1. Make sure you have Heroku CLI installed"
    echo "   Download: https://devcenter.heroku.com/articles/heroku-cli"
    echo ""
    echo "2. Run these commands:"
    echo ""
    echo "   heroku login"
    echo "   heroku create waks-bitcoin-miner-YOURNAME"
    echo "   git push heroku main"
    echo "   heroku open"
    echo ""
    ;;
  2)
    echo ""
    echo "Deploying to Railway.app..."
    echo ""
    echo "1. Go to https://railway.app"
    echo "2. Click 'New Project'"
    echo "3. Select 'Deploy from GitHub'"
    echo "4. Authorize and select ashermohamed546-arch/Waks"
    echo "5. Click 'Deploy'"
    echo ""
    echo "Railway will automatically build and deploy your app!"
    echo ""
    ;;
  3)
    echo ""
    echo "Deploying to Replit..."
    echo ""
    echo "1. Go to https://replit.com"
    echo "2. Click 'Import from GitHub'"
    echo "3. Paste: https://github.com/ashermohamed546-arch/Waks"
    echo "4. Click 'Import'"
    echo "5. Click 'Run'"
    echo ""
    echo "Your app will be live in seconds!"
    echo ""
    ;;
  4)
    echo ""
    echo "Building Docker image..."
    docker build -t waks-bitcoin-miner .
    echo ""
    echo "Run locally:"
    echo "  docker run -p 5000:5000 waks-bitcoin-miner"
    echo ""
    echo "Push to Docker Hub:"
    echo "  docker tag waks-bitcoin-miner yourusername/waks-bitcoin-miner"
    echo "  docker push yourusername/waks-bitcoin-miner"
    echo ""
    ;;
  *)
    echo "Invalid option"
    ;;
esac

echo "====================================="
echo "Need help? Check DEPLOY.md"
echo "====================================="
