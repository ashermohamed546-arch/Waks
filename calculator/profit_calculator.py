#!/usr/bin/env python3
"""
Profit Calculator - Calculate mining profits and ROI
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from .converter import BitcoinConverter

logger = logging.getLogger(__name__)


class ProfitCalculator:
    """Calculate mining profits and return on investment"""
    
    def __init__(self, converter: BitcoinConverter = None):
        """
        Initialize profit calculator
        
        Args:
            converter: BitcoinConverter instance
        """
        self.converter = converter or BitcoinConverter()
        logger.info("ProfitCalculator initialized")
    
    def calculate_mining_profit(self, btc_mined: float, currency: str = 'USD',
                               electricity_cost: float = 0,
                               hardware_cost: float = 0) -> Dict:
        """
        Calculate mining profit
        
        Args:
            btc_mined: Bitcoin mined
            currency: Currency for calculations
            electricity_cost: Total electricity cost
            hardware_cost: Hardware investment cost
            
        Returns:
            dict: Profit calculation results
        """
        # Convert BTC to fiat
        conversion = self.converter.convert(btc_mined, currency)
        
        if not conversion['converted']:
            return {'error': 'Could not convert BTC to fiat'}
        
        btc_value = conversion['converted']
        total_costs = electricity_cost + hardware_cost
        gross_profit = btc_value - electricity_cost  # Don't deduct hardware for ongoing
        net_profit = btc_value - total_costs
        roi_percent = (net_profit / hardware_cost * 100) if hardware_cost > 0 else 0
        
        return {
            'btc_mined': btc_mined,
            'btc_value': btc_value,
            'currency': currency,
            'electricity_cost': electricity_cost,
            'hardware_cost': hardware_cost,
            'gross_profit': round(gross_profit, 2),
            'net_profit': round(net_profit, 2),
            'roi_percent': round(roi_percent, 2),
            'breakeven_btc': round(total_costs / conversion['rate'], 8) if conversion['rate'] > 0 else 0
        }
    
    def calculate_hashrate_profit(self, hashrate_mh: float,
                                 difficulty: int,
                                 block_reward: float = 6.25,
                                 electricity_per_hour: float = 0.1,
                                 electricity_cost: float = 0.1,
                                 currency: str = 'USD',
                                 hours: float = 1) -> Dict:
        """
        Calculate profit based on hashrate
        
        Args:
            hashrate_mh: Hashrate in MH/s
            difficulty: Current mining difficulty
            block_reward: BTC per block
            electricity_per_hour: kWh per hour
            electricity_cost: Cost per kWh
            currency: Currency for calculations
            hours: Number of hours to calculate
            
        Returns:
            dict: Profit calculation
        """
        # Estimate BTC earned
        # This is a simplified calculation
        btc_per_hour = (hashrate_mh * 1e6) / (difficulty * 2**32) * block_reward
        btc_earned = btc_per_hour * hours
        
        # Calculate costs
        electricity_used = electricity_per_hour * hours
        electricity_cost_total = electricity_used * electricity_cost
        
        # Convert to fiat
        conversion = self.converter.convert(btc_earned, currency)
        
        if not conversion['converted']:
            return {'error': 'Could not convert BTC to fiat'}
        
        value = conversion['converted']
        profit = value - electricity_cost_total
        profit_per_hour = profit / hours if hours > 0 else 0
        
        return {
            'hashrate_mh': hashrate_mh,
            'difficulty': difficulty,
            'hours': hours,
            'btc_earned': round(btc_earned, 8),
            'btc_value': round(value, 2),
            'currency': currency,
            'electricity_used_kwh': round(electricity_used, 2),
            'electricity_cost': round(electricity_cost_total, 2),
            'gross_profit': round(value, 2),
            'net_profit': round(profit, 2),
            'profit_per_hour': round(profit_per_hour, 2),
            'btc_price': conversion['rate']
        }
    
    def calculate_payback_period(self, daily_profit: float,
                                hardware_cost: float) -> Optional[Dict]:
        """
        Calculate hardware payback period
        
        Args:
            daily_profit: Daily profit in fiat currency
            hardware_cost: Hardware investment cost
            
        Returns:
            dict: Payback period information
        """
        if daily_profit <= 0:
            return {
                'payback_possible': False,
                'reason': 'Daily profit is zero or negative'
            }
        
        days_to_payback = hardware_cost / daily_profit
        
        return {
            'payback_possible': True,
            'days': round(days_to_payback, 2),
            'weeks': round(days_to_payback / 7, 2),
            'months': round(days_to_payback / 30, 2),
            'payback_date': (datetime.now() + timedelta(days=days_to_payback)).date().isoformat(),
            'hardware_cost': hardware_cost,
            'daily_profit': daily_profit
        }
    
    def compare_currencies(self, btc_amount: float,
                          currencies: list = None) -> Dict:
        """
        Compare BTC value across multiple currencies
        
        Args:
            btc_amount: Amount in BTC
            currencies: List of currency codes
            
        Returns:
            dict: Comparison results
        """
        if currencies is None:
            currencies = ['USD', 'EUR', 'GBP', 'UGX', 'INR']  # Default including UGX
        
        results = {}
        
        for currency in currencies:
            try:
                conversion = self.converter.convert(btc_amount, currency)
                if conversion['converted']:
                    results[currency] = {
                        'value': conversion['converted'],
                        'rate': conversion['rate'],
                        'symbol': conversion['symbol'],
                        'formatted': conversion['formatted']
                    }
            except Exception as e:
                logger.error(f"Error converting to {currency}: {e}")
        
        return {
            'btc_amount': btc_amount,
            'conversions': results,
            'timestamp': datetime.now().isoformat()
        }
