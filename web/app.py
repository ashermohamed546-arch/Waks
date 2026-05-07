#!/usr/bin/env python3
"""
Waks Web Dashboard - Flask Application
Real-time Bitcoin mining monitor with calculator and mobile money transfers
"""

from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
import logging
from datetime import datetime
import json
import os
from functools import wraps

from calculator.converter import BitcoinConverter
from calculator.mobile_money import MobileMoneyTransfer
from calculator.profit_calculator import ProfitCalculator
from calculator.rates import ExchangeRateManager

logger = logging.getLogger(__name__)


def create_app(config=None):
    """
    Create and configure Flask application
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Flask: Configured Flask app
    """
    app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
    
    # Configuration
    if config:
        app.config['SECRET_KEY'] = config.get('web', {}).get('secret_key', 'dev-key-change-in-production')
        app.config['JSON_SORT_KEYS'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    else:
        app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    
    # Enable CORS
    CORS(app)
    
    # Initialize services
    converter = BitcoinConverter(config.get('calculator', {}) if config else {})
    mobile_money = MobileMoneyTransfer(converter)
    profit_calculator = ProfitCalculator(converter)
    rate_manager = ExchangeRateManager()
    
    # Store in app context
    app.converter = converter
    app.mobile_money = mobile_money
    app.profit_calculator = profit_calculator
    app.rate_manager = rate_manager
    
    # Middleware
    @app.before_request
    def before_request():
        """Initialize session if needed"""
        if 'user_id' not in session:
            session['user_id'] = os.urandom(16).hex()
    
    # ==================== HOME & DASHBOARD ====================
    
    @app.route('/')
    def index():
        """Main dashboard page"""
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Dashboard"""
        return render_template('dashboard.html')
    
    @app.route('/calculator')
    def calculator():
        """Calculator page"""
        return render_template('calculator.html')
    
    @app.route('/mobile-money')
    def mobile_money_page():
        """Mobile money transfer page"""
        return render_template('mobile_money.html')
    
    @app.route('/wallet')
    def wallet():
        """Wallet management page"""
        return render_template('wallet.html')
    
    # ==================== API: MINING STATS ====================
    
    @app.route('/api/health')
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/mining/stats')
    def mining_stats():
        """Get mining statistics"""
        # In real implementation, this would get actual miner stats
        return jsonify({
            'status': 'ok',
            'data': {
                'hashrate': '2.45 MH/s',
                'blocks': 12,
                'shares': 156,
                'difficulty': 4,
                'uptime': '2 days 14 hours',
                'btc_earned': 0.00452,
                'last_block': '2026-05-07T20:30:00Z'
            }
        })
    
    @app.route('/api/mining/history')
    def mining_history():
        """Get mining history"""
        return jsonify({
            'status': 'ok',
            'data': {
                'total_hashes': 1234567890,
                'valid_hashes': 234,
                'blocks_found': 12,
                'shares_accepted': 156,
                'shares_rejected': 4
            }
        })
    
    # ==================== API: CALCULATOR ====================
    
    @app.route('/api/calculator/convert', methods=['GET', 'POST'])
    def convert_btc():
        """Convert BTC to fiat currency"""
        try:
            # Get parameters
            if request.method == 'POST':
                data = request.get_json()
                btc_amount = float(data.get('btc', 0))
                currency = data.get('currency', 'USD').upper()
            else:
                btc_amount = float(request.args.get('btc', 0))
                currency = request.args.get('currency', 'USD').upper()
            
            # Validate
            if btc_amount <= 0:
                return jsonify({'error': 'Invalid BTC amount'}), 400
            
            # Convert
            result = app.converter.convert(btc_amount, currency)
            
            return jsonify({
                'status': 'ok',
                'data': result
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            return jsonify({'error': 'Conversion failed'}), 500
    
    @app.route('/api/calculator/convert-multiple', methods=['POST'])
    def convert_multiple():
        """Convert BTC to multiple currencies"""
        try:
            data = request.get_json()
            btc_amount = float(data.get('btc', 0))
            currencies = data.get('currencies', ['USD', 'EUR', 'GBP', 'UGX'])
            
            results = app.converter.convert_multiple(btc_amount, currencies)
            
            return jsonify({
                'status': 'ok',
                'data': results
            })
        except Exception as e:
            logger.error(f"Multi-conversion error: {e}")
            return jsonify({'error': 'Conversion failed'}), 500
    
    @app.route('/api/calculator/rates')
    def get_rates():
        """Get exchange rates for multiple currencies"""
        try:
            currencies = request.args.getlist('currencies')
            if not currencies:
                currencies = ['USD', 'EUR', 'GBP', 'UGX', 'KES', 'NGN']
            
            rates = app.rate_manager.get_rates(currencies)
            
            return jsonify({
                'status': 'ok',
                'data': rates,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Rate fetch error: {e}")
            return jsonify({'error': 'Could not fetch rates'}), 500
    
    @app.route('/api/calculator/profit', methods=['POST'])
    def calculate_profit():
        """Calculate mining profit"""
        try:
            data = request.get_json()
            
            btc_mined = float(data.get('btc_mined', 0))
            currency = data.get('currency', 'USD').upper()
            electricity_cost = float(data.get('electricity_cost', 0))
            hardware_cost = float(data.get('hardware_cost', 0))
            
            result = app.profit_calculator.calculate_mining_profit(
                btc_mined=btc_mined,
                currency=currency,
                electricity_cost=electricity_cost,
                hardware_cost=hardware_cost
            )
            
            return jsonify({
                'status': 'ok',
                'data': result
            })
        except Exception as e:
            logger.error(f"Profit calculation error: {e}")
            return jsonify({'error': 'Calculation failed'}), 500
    
    # ==================== API: MOBILE MONEY ====================
    
    @app.route('/api/mobile-money/providers')
    def get_providers():
        """Get available mobile money providers"""
        try:
            providers = {}
            for provider in ['MTN', 'AIRTEL', 'UGANDA_TELECOM', 'ORANGE', 'VODAFONE', 'SAFARICOM']:
                providers[provider] = app.mobile_money.get_provider_info(provider)
            
            return jsonify({
                'status': 'ok',
                'data': providers
            })
        except Exception as e:
            logger.error(f"Provider fetch error: {e}")
            return jsonify({'error': 'Could not fetch providers'}), 500
    
    @app.route('/api/mobile-money/providers/<provider>')
    def get_provider_info(provider):
        """Get specific provider information"""
        try:
            info = app.mobile_money.get_provider_info(provider.upper())
            
            return jsonify({
                'status': 'ok',
                'data': info
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/mobile-money/currencies')
    def get_supported_currencies():
        """Get supported currencies for mobile money"""
        return jsonify({
            'status': 'ok',
            'data': MobileMoneyTransfer.SUPPORTED_CURRENCIES
        })
    
    @app.route('/api/mobile-money/transfer', methods=['POST'])
    def initiate_transfer():
        """Initiate mobile money transfer"""
        try:
            data = request.get_json()
            
            btc_amount = float(data.get('btc'))
            phone_number = data.get('phone')
            provider = data.get('provider', '').upper()
            currency = data.get('currency', '').upper()
            
            # Get current rate
            rate = app.rate_manager.get_rate(currency)
            if not rate:
                return jsonify({'error': f'Could not get rate for {currency}'}), 400
            
            # Initiate transfer
            result = app.mobile_money.initiate_transfer(
                btc_amount=btc_amount,
                phone_number=phone_number,
                provider=provider,
                currency=currency,
                btc_rate=rate,
                user_id=session.get('user_id')
            )
            
            if 'error' in result:
                return jsonify({'error': result['error']}), 400
            
            return jsonify({
                'status': 'ok',
                'data': result
            })
        except ValueError as e:
            return jsonify({'error': f'Invalid input: {str(e)}'}), 400
        except Exception as e:
            logger.error(f"Transfer initiation error: {e}")
            return jsonify({'error': 'Transfer initiation failed'}), 500
    
    @app.route('/api/mobile-money/transfer/<transaction_id>/confirm', methods=['POST'])
    def confirm_transfer(transaction_id):
        """Confirm mobile money transfer"""
        try:
            data = request.get_json()
            confirmation_code = data.get('confirmation_code')
            
            result = app.mobile_money.confirm_transfer(transaction_id, confirmation_code)
            
            if 'error' in result:
                return jsonify({'error': result['error']}), 400
            
            return jsonify({
                'status': 'ok',
                'data': result
            })
        except Exception as e:
            logger.error(f"Transfer confirmation error: {e}")
            return jsonify({'error': 'Confirmation failed'}), 500
    
    @app.route('/api/mobile-money/transfer/<transaction_id>')
    def get_transfer_status(transaction_id):
        """Get transfer status"""
        try:
            status = app.mobile_money.get_transaction_status(transaction_id)
            
            if 'error' in status:
                return jsonify({'error': status['error']}), 404
            
            return jsonify({
                'status': 'ok',
                'data': status
            })
        except Exception as e:
            logger.error(f"Status fetch error: {e}")
            return jsonify({'error': 'Could not fetch status'}), 500
    
    @app.route('/api/mobile-money/transfer/<transaction_id>/confirm', methods=['GET'])
    def get_transfer_confirm_page(transaction_id):
        """Get confirmation details for transfer"""
        try:
            status = app.mobile_money.get_transaction_status(transaction_id)
            
            if 'error' in status:
                return jsonify({'error': status['error']}), 404
            
            return jsonify({
                'status': 'ok',
                'data': {
                    'transaction_id': transaction_id,
                    'phone': status.get('phone_number'),
                    'provider': status.get('provider'),
                    'amount': f"{status.get('net_amount')} {status.get('currency')}",
                    'fee': f"{status.get('fee_amount')} {status.get('currency')}"
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/mobile-money/history')
    def get_transfer_history():
        """Get transfer history for current user"""
        try:
            user_id = session.get('user_id')
            limit = request.args.get('limit', 10, type=int)
            
            history = app.mobile_money.get_transfer_history(user_id=user_id, limit=limit)
            
            return jsonify({
                'status': 'ok',
                'data': history
            })
        except Exception as e:
            logger.error(f"History fetch error: {e}")
            return jsonify({'error': 'Could not fetch history'}), 500
    
    @app.route('/api/mobile-money/estimate', methods=['POST'])
    def estimate_transfer():
        """Estimate BTC needed for transfer"""
        try:
            data = request.get_json()
            
            fiat_amount = float(data.get('amount'))
            provider = data.get('provider', '').upper()
            
            # Get current rate
            rates = app.rate_manager.get_rates(['USD'])  # Get USD as base
            if not rates or 'USD' not in rates:
                return jsonify({'error': 'Could not fetch rates'}), 400
            
            btc_rate = rates['USD']
            
            result = app.mobile_money.estimate_btc_amount_for_transfer(
                fiat_amount=fiat_amount,
                provider=provider,
                btc_rate=btc_rate
            )
            
            return jsonify({
                'status': 'ok',
                'data': result
            })
        except Exception as e:
            logger.error(f"Estimation error: {e}")
            return jsonify({'error': 'Estimation failed'}), 500
    
    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        logger.error(f"Server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # ==================== STATIC PAGES ====================
    
    @app.route('/api/info')
    def app_info():
        """Get application information"""
        return jsonify({
            'name': 'Waks',
            'version': '1.0.0',
            'description': 'Bitcoin Miner with Calculator & Mobile Money Transfer',
            'features': [
                'CPU Mining',
                'Bitcoin Calculator',
                'Mobile Money Transfer',
                'Real-time Exchange Rates',
                'Profit Calculator'
            ],
            'supported_providers': ['MTN', 'AIRTEL', 'UGANDA_TELECOM', 'ORANGE', 'VODAFONE', 'SAFARICOM'],
            'supported_currencies': list(BitcoinConverter.SUPPORTED_CURRENCIES.keys())
        })
    
    return app
