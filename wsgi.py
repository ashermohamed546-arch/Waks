#!/usr/bin/env python3
"""
Heroku startup script
Automatically runs when deployed to Heroku
"""

import os
import json
from web.app import create_app

# Ensure config.json exists
if not os.path.exists('config.json'):
    print("Creating config.json from template...")
    if os.path.exists('config_template.json'):
        import shutil
        shutil.copy('config_template.json', 'config.json')
    else:
        # Create minimal config
        config = {
            "mining": {
                "enabled": True,
                "threads": 2,
                "mode": "cpu",
                "difficulty": 4,
                "auto_adjust_difficulty": True,
                "update_interval": 60
            },
            "pool": {
                "enabled": False,
                "server": "stratum.mining.com",
                "port": 3333,
                "username": "username.worker1",
                "password": "password",
                "reconnect_interval": 30,
                "max_reconnect_attempts": 10
            },
            "wallet": {
                "address": "1A1z7agoat3...",
                "private_key": "",
                "network": "mainnet"
            },
            "calculator": {
                "enabled": True,
                "default_currency": "USD",
                "supported_currencies": ["USD", "EUR", "GBP", "JPY", "UGX"],
                "update_rate_interval": 300,
                "api_source": "coingecko"
            },
            "web": {
                "enabled": True,
                "host": "0.0.0.0",
                "port": int(os.environ.get('PORT', 5000)),
                "debug": False,
                "secret_key": os.environ.get('SECRET_KEY', 'heroku-secret-key'),
                "ssl": False,
                "cert_path": "",
                "key_path": ""
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/waks.log",
                "max_size": 10485760,
                "backup_count": 5
            },
            "hardware": {
                "cpu_affinity": True,
                "nice_level": 0,
                "max_temperature": 85,
                "gpu_mining": False,
                "gpu_device": 0
            },
            "performance": {
                "optimize_hash": True,
                "use_sse2": True,
                "use_avx": True,
                "cache_optimization": True,
                "batch_size": 1000
            }
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Update port from environment
config['web']['port'] = int(os.environ.get('PORT', 5000))
config['web']['secret_key'] = os.environ.get('SECRET_KEY', 'change-me')

# Create Flask app
app = create_app(config)

if __name__ == '__main__':
    # Run on Heroku
    port = int(os.environ.get('PORT', 5000))
    print(f"\n{'='*60}")
    print(f"Waks - Bitcoin Miner")
    print(f"{'='*60}")
    print(f"Starting on 0.0.0.0:{port}")
    print(f"Visit: http://localhost:{port}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
