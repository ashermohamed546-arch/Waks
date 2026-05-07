#!/usr/bin/env python3
"""
Exchange Rate Manager
Fetches and caches Bitcoin exchange rates
"""

import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import json

logger = logging.getLogger(__name__)


class ExchangeRateManager:
    """Manage Bitcoin exchange rates"""
    
    # CoinGecko API endpoint (free, no auth required)
    COINGECKO_API = 'https://api.coingecko.com/api/v3'
    
    # Cache duration in seconds
    CACHE_DURATION = 300  # 5 minutes
    
    def __init__(self):
        """
        Initialize rate manager
        """
        self.rates_cache = {}
        self.cache_timestamp = {}
        logger.info("ExchangeRateManager initialized")
    
    def get_rate(self, currency: str) -> Optional[float]:
        """
        Get Bitcoin to currency exchange rate
        
        Args:
            currency: Currency code (e.g., 'USD', 'EUR', 'UGX')
            
        Returns:
            float: Exchange rate or None if unavailable
        """
        # Check cache
        if self._is_cache_valid(currency):
            logger.debug(f"Using cached rate for {currency}")
            return self.rates_cache.get(currency)
        
        # Fetch from API
        try:
            rate = self._fetch_rate_coingecko(currency)
            if rate:
                self.rates_cache[currency] = rate
                self.cache_timestamp[currency] = datetime.now()
                return rate
        except Exception as e:
            logger.error(f"Error fetching rate for {currency}: {e}")
        
        return None
    
    def get_rates(self, currencies: List[str]) -> Dict[str, float]:
        """
        Get rates for multiple currencies
        
        Args:
            currencies: List of currency codes
            
        Returns:
            dict: Dictionary of {currency: rate}
        """
        rates = {}
        for currency in currencies:
            rate = self.get_rate(currency)
            if rate:
                rates[currency] = rate
        return rates
    
    def _fetch_rate_coingecko(self, currency: str) -> Optional[float]:
        """
        Fetch rate from CoinGecko API
        
        Args:
            currency: Currency code
            
        Returns:
            float: Exchange rate or None
        """
        try:
            currency_lower = currency.lower()
            url = f"{self.COINGECKO_API}/simple/price"
            params = {
                'ids': 'bitcoin',
                'vs_currencies': currency_lower,
                'include_market_cap': 'false',
                'include_24hr_vol': 'false',
                'include_last_updated_at': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rate = data.get('bitcoin', {}).get(currency_lower)
            
            if rate:
                logger.info(f"Fetched rate for {currency}: 1 BTC = {rate:,.2f} {currency}")
            
            return rate
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing API response: {e}")
            return None
    
    def _is_cache_valid(self, currency: str) -> bool:
        """
        Check if cached rate is still valid
        
        Args:
            currency: Currency code
            
        Returns:
            bool: True if cache is valid
        """
        if currency not in self.cache_timestamp:
            return False
        
        age = datetime.now() - self.cache_timestamp[currency]
        return age < timedelta(seconds=self.CACHE_DURATION)
    
    def get_historical_rate(self, currency: str, days: int = 7) -> Optional[List[Dict]]:
        """
        Get historical exchange rates
        
        Args:
            currency: Currency code
            days: Number of days of history
            
        Returns:
            list: List of historical rates with dates
        """
        try:
            currency_lower = currency.lower()
            url = f"{self.COINGECKO_API}/coins/bitcoin/market_chart"
            params = {
                'vs_currency': currency_lower,
                'days': days,
                'interval': 'daily'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            prices = data.get('prices', [])
            
            # Convert to readable format
            history = []
            for timestamp, price in prices:
                dt = datetime.fromtimestamp(timestamp / 1000)
                history.append({
                    'date': dt.date().isoformat(),
                    'price': price,
                    'currency': currency
                })
            
            logger.info(f"Fetched {len(history)} days of historical data for {currency}")
            return history
            
        except Exception as e:
            logger.error(f"Error fetching historical rates: {e}")
            return None
    
    def clear_cache(self, currency: str = None):
        """
        Clear rate cache
        
        Args:
            currency: Specific currency to clear (clears all if None)
        """
        if currency:
            if currency in self.rates_cache:
                del self.rates_cache[currency]
            if currency in self.cache_timestamp:
                del self.cache_timestamp[currency]
            logger.info(f"Cleared cache for {currency}")
        else:
            self.rates_cache.clear()
            self.cache_timestamp.clear()
            logger.info("Cleared all rate cache")
