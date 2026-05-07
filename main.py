#!/usr/bin/env python3
"""
Waks - Bitcoin Miner with Calculator
Main entry point for the application
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Import core modules
from core.miner import BitcoinMiner
from calculator.converter import BitcoinConverter
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
        description='Waks - Bitcoin Miner with Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  CPU Mining:           python main.py --mode cpu --threads 4
  Pool Mining:          python main.py --mode pool --pool stratum.mining.com
  Web Dashboard Only:   python main.py --web --port 5000
  Calculator:           python main.py --calculator --amount 0.5 --currency USD
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
