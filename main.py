#!/usr/bin/env python3
"""
Waks - Bitcoin Miner with Calculator
Updated main entry point with mobile money transfer support
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Import core modules
from core.miner import BitcoinMiner
from calculator.converter import BitcoinConverter
from calculator.mobile_money import MobileMoneyTransfer
from web.app import create_app
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path='config.json'):
    """Load configuration from JSON file"""
    if not Path(config_path).exists():
        logger.error(f"Configuration file not found: {config_path}")
        logger.info("Creating from template...")
        if Path('config_template.json').exists():
            import shutil
            shutil.copy('config_template.json', config_path)
        else:
            sys.exit(1)
    
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description='Waks - Bitcoin Miner with Calculator & Mobile Money Transfer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  CPU Mining:                python main.py --mode cpu --threads 4
  Pool Mining:               python main.py --mode pool --pool stratum.mining.com
  Web Dashboard Only:        python main.py --web --port 5000
  Calculator:                python main.py --calculator --amount 0.5 --currency USD
  Mobile Money Transfer:     python main.py --mobile-money --btc 0.1 --phone +256700000000 --provider MTN --currency UGX
  Transfer Status:           python main.py --mobile-money --status TX-ABC123
        """
    )
    
    # General arguments
    parser.add_argument('--config', default='config.json', 
                        help='Path to configuration file')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    
    # Mining arguments
    parser.add_argument('--mode', choices=['cpu', 'gpu', 'pool', 'hybrid'],
                        default='cpu',
                        help='Mining mode (default: cpu)')
    parser.add_argument('--threads', type=int,
                        help='Number of mining threads')
    parser.add_argument('--difficulty', type=int,
                        help='Mining difficulty')
    
    # Pool arguments
    parser.add_argument('--pool', 
                        help='Mining pool address')
    parser.add_argument('--port', type=int,
                        help='Mining pool port')
    parser.add_argument('--worker',
                        help='Pool worker username')
    
    # Web interface arguments
    parser.add_argument('--web', action='store_true',
                        help='Start web dashboard')
    parser.add_argument('--web-port', type=int, default=5000,
                        help='Web server port (default: 5000)')
    parser.add_argument('--web-host', default='0.0.0.0',
                        help='Web server host (default: 0.0.0.0)')
    
    # Calculator arguments
    parser.add_argument('--calculator', action='store_true',
                        help='Run calculator only')
    parser.add_argument('--amount', type=float,
                        help='Bitcoin amount to convert')
    parser.add_argument('--currency', default='USD',
                        help='Target currency (default: USD)')
    
    # Mobile Money arguments
    parser.add_argument('--mobile-money', action='store_true',
                        help='Mobile money transfer mode')
    parser.add_argument('--btc', type=float,
                        help='BTC amount to transfer')
    parser.add_argument('--phone',
                        help='Recipient phone number')
    parser.add_argument('--provider',
                        help='Mobile money provider (MTN, AIRTEL, UGANDA_TELECOM, etc.)')
    parser.add_argument('--status',
                        help='Check transfer status by transaction ID')
    parser.add_argument('--history', action='store_true',
                        help='Show transfer history')
    parser.add_argument('--providers', action='store_true',
                        help='List available providers and supported currencies')
    
    # Status/Info arguments
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--info', action='store_true',
                        help='Show system information and exit')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    # Show system info
    if args.info:
        from core.utils import show_system_info
        show_system_info()
        sys.exit(0)
    
    # Mobile Money Transfer mode
    if args.mobile_money:
        converter = BitcoinConverter(config['calculator'])
        mobile_money = MobileMoneyTransfer(converter)
        
        # List providers
        if args.providers:
            print("\n" + "="*70)
            print("AVAILABLE MOBILE MONEY PROVIDERS")
            print("="*70)
            
            for provider in ['MTN', 'AIRTEL', 'UGANDA_TELECOM', 'ORANGE', 'VODAFONE', 'SAFARICOM']:
                info = mobile_money.get_provider_info(provider)
                print(f"\n{info['name']}")
                print(f"  Fee Rate:              {info['fee_rate']}")
                print(f"  Min Amount:            {info['min_amount']}")
                print(f"  Max Amount:            {info['max_amount']}")
                print(f"  Supported Currencies:  {', '.join(info['supported_currencies'])}")
                print(f"  {info['description']}")
            
            print("\n" + "="*70 + "\n")
            sys.exit(0)
        
        # Check status
        if args.status:
            status = mobile_money.get_transaction_status(args.status)
            print("\n" + "="*70)
            print(f"TRANSFER STATUS: {args.status}")
            print("="*70)
            if 'error' in status:
                print(f"Error: {status['error']}")
            else:
                print(f"Status:        {status.get('status')}")
                print(f"BTC Amount:    {status.get('btc_amount')} BTC")
                print(f"Fiat Amount:   {status.get('fiat_amount')} {status.get('currency')}")
                print(f"Provider:      {status.get('provider')}")
                print(f"Phone:         {status.get('phone_number')}")
                print(f"Reference:     {status.get('reference', 'N/A')}")
            print("="*70 + "\n")
            sys.exit(0)
        
        # Show history
        if args.history:
            history = mobile_money.get_transfer_history()
            print("\n" + "="*70)
            print("TRANSFER HISTORY")
            print("="*70)
            if not history:
                print("No transfers found.")
            else:
                for tx in history:
                    print(f"\n{tx['id']} - {tx['status'].upper()}")
                    print(f"  {tx['btc_amount']} BTC -> {tx['net_amount']} {tx['currency']}")
                    print(f"  Provider: {tx['provider']}")
                    print(f"  Date: {tx['timestamp']}")
            print("\n" + "="*70 + "\n")
            sys.exit(0)
        
        # Initiate transfer
        if args.btc and args.phone and args.provider and args.currency:
            # Get current BTC rate
            rate = converter.rate_manager.get_rate(args.currency)
            if not rate:
                print(f"Error: Could not get exchange rate for {args.currency}")
                sys.exit(1)
            
            result = mobile_money.initiate_transfer(
                btc_amount=args.btc,
                phone_number=args.phone,
                provider=args.provider,
                currency=args.currency,
                btc_rate=rate
            )
            
            print("\n" + "="*70)
            print("MOBILE MONEY TRANSFER")
            print("="*70)
            if 'error' in result:
                print(f"Error: {result['error']}")
            else:
                details = result['details']
                print(f"Status:            {result['status']}")
                print(f"Transaction ID:    {result['transaction_id']}")
                print(f"BTC Amount:        {details['btc_amount']} BTC")
                print(f"Fiat Amount:       {details['fiat_amount']} {details['currency']}")
                print(f"Provider:          {details['provider']}")
                print(f"Fee ({details['fee_rate']}):  {details['fee_amount']} {details['currency']}")
                print(f"You Receive:       {details['net_amount']} {details['currency']}")
                print(f"\n{result['message']}")
            print("="*70 + "\n")
            sys.exit(0)
        
        print("\nMobile money mode requires: --btc, --phone, --provider, --currency")
        print("Use --providers to see available options")
        sys.exit(1)
    
    # Calculator-only mode
    if args.calculator:
        converter = BitcoinConverter(config['calculator'])
        if args.amount:
            result = converter.convert(args.amount, args.currency)
            print(f"\n{'='*50}")
            print(f"{args.amount} BTC = {result['converted']} {result['currency']}")
            print(f"Rate: {result['rate']} {result['currency']}/BTC")
            print(f"Updated: {result['timestamp']}")
            print(f"{'='*50}\n")
        else:
            # Interactive calculator
            converter.interactive_mode()
        sys.exit(0)
    
    # Web-only mode
    if args.web:
        logger.info(f"Starting web dashboard on {args.web_host}:{args.web_port}")
        app = create_app(config)
        app.run(host=args.web_host, port=args.web_port, 
                debug=args.debug, use_reloader=False)
        sys.exit(0)
    
    # Mining mode
    logger.info(f"Starting Bitcoin Miner in {args.mode} mode")
    
    # Override config with command line arguments
    if args.threads:
        config['mining']['threads'] = args.threads
    if args.difficulty:
        config['mining']['difficulty'] = args.difficulty
    if args.pool:
        config['pool']['server'] = args.pool
    if args.port:
        config['pool']['port'] = args.port
    if args.worker:
        config['pool']['username'] = args.worker
    
    # Create and start miner
    miner = BitcoinMiner(config, mode=args.mode)
    
    try:
        miner.start()
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        miner.stop()
        logger.info("Miner stopped.")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
