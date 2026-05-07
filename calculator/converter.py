#!/usr/bin/env python3
"""
Bitcoin to Fiat Converter
Supports multiple currencies including Ugandan Shilling (UGX)
"""

import logging
from datetime import datetime
from typing import Dict, Optional, List
from .rates import ExchangeRateManager

logger = logging.getLogger(__name__)


class BitcoinConverter:
    """Convert Bitcoin to various fiat currencies"""
    
    # Supported currencies
    SUPPORTED_CURRENCIES = {
        'USD': {'name': 'US Dollar', 'symbol': '$'},
        'EUR': {'name': 'Euro', 'symbol': '€'},
        'GBP': {'name': 'British Pound', 'symbol': '£'},
        'JPY': {'name': 'Japanese Yen', 'symbol': '¥'},
        'AUD': {'name': 'Australian Dollar', 'symbol': 'A$'},
        'CAD': {'name': 'Canadian Dollar', 'symbol': 'C$'},
        'CHF': {'name': 'Swiss Franc', 'symbol': 'Fr'},
        'CNY': {'name': 'Chinese Yuan', 'symbol': '¥'},
        'INR': {'name': 'Indian Rupee', 'symbol': '₹'},
        'SEK': {'name': 'Swedish Krona', 'symbol': 'kr'},
        'NZD': {'name': 'New Zealand Dollar', 'symbol': 'NZ$'},
        'MXN': {'name': 'Mexican Peso', 'symbol': '$'},
        'SGD': {'name': 'Singapore Dollar', 'symbol': 'S$'},
        'HKD': {'name': 'Hong Kong Dollar', 'symbol': 'HK$'},
        'NOK': {'name': 'Norwegian Krone', 'symbol': 'kr'},
        'KRW': {'name': 'South Korean Won', 'symbol': '₩'},
        'TRY': {'name': 'Turkish Lira', 'symbol': '₺'},
        'BRL': {'name': 'Brazilian Real', 'symbol': 'R$'},
        'ZAR': {'name': 'South African Rand', 'symbol': 'R'},
        'UGX': {'name': 'Ugandan Shilling', 'symbol': 'USh'},  # ✅ UGANDA
        'KES': {'name': 'Kenyan Shilling', 'symbol': 'KSh'},
        'NGN': {'name': 'Nigerian Naira', 'symbol': '₦'},
        'GHS': {'name': 'Ghanaian Cedi', 'symbol': '₵'},
        'EGP': {'name': 'Egyptian Pound', 'symbol': '£'},
    }
    
    def __init__(self, config: Dict = None):
        """
        Initialize converter
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.rate_manager = ExchangeRateManager()
        self.default_currency = config.get('default_currency', 'USD') if config else 'USD'
        
        logger.info(f"BitcoinConverter initialized (default: {self.default_currency})")
    
    def convert(self, btc_amount: float, target_currency: str = None) -> Dict:
        """
        Convert Bitcoin to fiat currency
        
        Args:
            btc_amount: Amount in BTC
            target_currency: Target currency code (uses default if None)
            
        Returns:
            dict: Conversion result with rate and converted amount
        """
        target_currency = target_currency or self.default_currency
        
        if target_currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {target_currency}")
        
        # Get exchange rate
        rate = self.rate_manager.get_rate(target_currency)
        
        if rate is None:
            logger.warning(f"Could not get rate for {target_currency}")
            return {
                'btc': btc_amount,
                'currency': target_currency,
                'converted': None,
                'rate': None,
                'error': f'Could not fetch rate for {target_currency}',
                'timestamp': datetime.now().isoformat()
            }
        
        converted = btc_amount * rate
        
        return {
            'btc': btc_amount,
            'currency': target_currency,
            'currency_name': self.SUPPORTED_CURRENCIES[target_currency]['name'],
            'symbol': self.SUPPORTED_CURRENCIES[target_currency]['symbol'],
            'converted': round(converted, 2),
            'rate': rate,
            'formatted': f"{self.SUPPORTED_CURRENCIES[target_currency]['symbol']}{converted:,.2f}",
            'timestamp': datetime.now().isoformat()
        }
    
    def convert_multiple(self, btc_amount: float, currencies: List[str] = None) -> List[Dict]:
        """
        Convert Bitcoin to multiple currencies
        
        Args:
            btc_amount: Amount in BTC
            currencies: List of currency codes (uses defaults if None)
            
        Returns:
            list: List of conversion results
        """
        if currencies is None:
            currencies = ['USD', 'EUR', 'GBP', 'UGX']  # Default currencies including UGX
        
        results = []
        for currency in currencies:
            try:
                result = self.convert(btc_amount, currency)
                results.append(result)
            except Exception as e:
                logger.error(f"Error converting to {currency}: {e}")
        
        return results
    
    def interactive_mode(self):
        """
        Run interactive calculator mode
        """
        print("\n" + "="*60)
        print("Bitcoin to Fiat Converter - Interactive Mode")
        print("="*60)
        print(f"\nSupported currencies: {', '.join(sorted(self.SUPPORTED_CURRENCIES.keys()))}")
        print("Type 'list' to see all currencies")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                # Get BTC amount
                btc_input = input("Enter BTC amount (or 'quit'): ").strip()
                
                if btc_input.lower() == 'quit':
                    print("\nGoodbye!\n")
                    break
                
                if btc_input.lower() == 'list':
                    self._print_currencies()
                    continue
                
                try:
                    btc_amount = float(btc_input)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue
                
                # Get currency
                currency = input("Enter currency code (default: USD): ").strip().upper() or 'USD'
                
                if currency not in self.SUPPORTED_CURRENCIES:
                    print(f"Unsupported currency: {currency}")
                    continue
                
                # Perform conversion
                result = self.convert(btc_amount, currency)
                
                print("\n" + "-"*60)
                print(f"Conversion Result:")
                print(f"  Input:        {result['btc']} BTC")
                print(f"  Rate:         1 BTC = {result['rate']:,.2f} {currency}")
                print(f"  Converted:    {result['formatted']}")
                print(f"  Updated:      {result['timestamp']}")
                print("-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!\n")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    @staticmethod
    def _print_currencies():
        """
        Print list of supported currencies
        """
        print("\nSupported Currencies:")
        print("-" * 50)
        
        currencies = BitcoinConverter.SUPPORTED_CURRENCIES
        
        # Group by region
        regions = {
            'Americas': ['USD', 'CAD', 'MXN', 'BRL'],
            'Europe': ['EUR', 'GBP', 'CHF', 'SEK', 'NOK', 'TRY'],
            'Asia Pacific': ['JPY', 'CNY', 'INR', 'SGD', 'HKD', 'KRW', 'AUD', 'NZD'],
            'Africa': ['ZAR', 'KES', 'NGN', 'GHS', 'EGP', 'UGX'],  # ✅ UGX in Africa
        }
        
        for region, codes in regions.items():
            print(f"\n{region}:")
            for code in codes:
                if code in currencies:
                    info = currencies[code]
                    print(f"  {code}: {info['name']} ({info['symbol']})")
    
    def get_portfolio_value(self, holdings: Dict[str, float], 
                           currency: str = None) -> Dict:
        """
        Calculate total portfolio value
        
        Args:
            holdings: Dictionary of {currency: amount}
            currency: Target currency for total (uses default if None)
            
        Returns:
            dict: Portfolio value
        """
        target_currency = currency or self.default_currency
        total_btc = sum(holdings.get('BTC', 0) for _ in [None])
        
        results = []
        total_value = 0
        
        for curr, amount in holdings.items():
            if curr == 'BTC':
                result = self.convert(amount, target_currency)
                if result['converted']:
                    total_value += result['converted']
                results.append(result)
        
        return {
            'total_value': round(total_value, 2),
            'target_currency': target_currency,
            'holdings': results,
            'timestamp': datetime.now().isoformat()
        }
