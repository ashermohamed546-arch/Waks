#!/usr/bin/env python3
"""
Web Dashboard - Flask web application
Monitor mining progress and manage Bitcoin calculator
"""

from flask import Flask, render_template, jsonify, request
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def create_app(config=None):
    """
    Create and configure Flask application
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Flask: Configured Flask app
    """
    app = Flask(__name__)
    
    # Configuration
    if config:
        app.config['SECRET_KEY'] = config.get('web', {}).get('secret_key', 'dev-key-change-in-production')
    else:
        app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    
    # Routes
    @app.route('/')
    def index():
        """Dashboard home page"""
        return jsonify({
            'status': 'ok',
            'app': 'Waks Bitcoin Miner',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/mining/stats')
    def mining_stats():
        """Get mining statistics"""
        return jsonify({
            'status': 'ok',
            'data': {
                'hashrate': '0 H/s',
                'blocks': 0,
                'shares': 0
            }
        })
    
    @app.route('/api/calculator/convert', methods=['GET', 'POST'])
    def convert():
        """Bitcoin conversion endpoint"""
        data = request.get_json() or request.args
        
        btc = data.get('btc', 0)
        currency = data.get('currency', 'USD')
        
        return jsonify({
            'status': 'ok',
            'btc': btc,
            'currency': currency,
            'converted': 0,
            'rate': 0
        })
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy'})
    
    return app
