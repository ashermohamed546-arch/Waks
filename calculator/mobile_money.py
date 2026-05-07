#!/usr/bin/env python3
"""
Mobile Money Transfer Integration
Support for MTN Mobile Money, Airtel Money, Uganda Telecom, and other providers
Allow users to withdraw mining earnings to mobile money accounts
"""

import logging
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class MobileMoneyProvider(Enum):
    """Mobile money service providers"""
    MTN = "mtn"  # MTN Mobile Money (Uganda, Ghana, Kenya, etc.)
    AIRTEL = "airtel"  # Airtel Money
    UGANDA_TELECOM = "utl"  # Uganda Telecom Money
    ORANGE = "orange"  # Orange Money
    VODAFONE = "vodafone"  # Vodafone Cash
    SAFARICOM = "safaricom"  # M-Pesa (Kenya)
    EQUITEL = "equitel"  # Equitel (Kenya)


class MobileMoneyTransfer:
    """Handle mobile money transfers for Bitcoin mining earnings"""
    
    SUPPORTED_CURRENCIES = {
        'UGX': {'name': 'Ugandan Shilling', 'providers': ['MTN', 'AIRTEL', 'UGANDA_TELECOM']},
        'KES': {'name': 'Kenyan Shilling', 'providers': ['SAFARICOM', 'AIRTEL']},
        'GHS': {'name': 'Ghanaian Cedi', 'providers': ['MTN', 'AIRTEL', 'VODAFONE']},
        'NGN': {'name': 'Nigerian Naira', 'providers': ['MTN', 'AIRTEL']},
        'EGP': {'name': 'Egyptian Pound', 'providers': ['ORANGE', 'VODAFONE']},
    }
    
    # Transaction fees (example rates)
    TRANSFER_FEES = {
        'MTN': 0.02,  # 2% fee
        'AIRTEL': 0.02,  # 2% fee
        'UGANDA_TELECOM': 0.025,  # 2.5% fee
        'ORANGE': 0.02,  # 2% fee
        'SAFARICOM': 0.025,  # 2.5% fee
    }
    
    # Minimum and maximum transfer amounts in USD equivalent
    LIMITS = {
        'MTN': {'min': 0.5, 'max': 500},
        'AIRTEL': {'min': 0.5, 'max': 500},
        'UGANDA_TELECOM': {'min': 1, 'max': 300},
        'ORANGE': {'min': 0.5, 'max': 400},
        'VODAFONE': {'min': 0.5, 'max': 300},
        'SAFARICOM': {'min': 0.5, 'max': 500},
    }
    
    def __init__(self, converter=None):
        """
        Initialize mobile money transfer manager
        
        Args:
            converter: BitcoinConverter instance for BTC to fiat conversion
        """
        self.converter = converter
        self.transaction_history = []
        logger.info("MobileMoneyTransfer initialized")
    
    def get_supported_providers(self, currency: str) -> List[str]:
        """
        Get supported providers for a currency
        
        Args:
            currency: Currency code (e.g., 'UGX')
            
        Returns:
            list: List of supported providers
        """
        if currency in self.SUPPORTED_CURRENCIES:
            return self.SUPPORTED_CURRENCIES[currency]['providers']
        return []
    
    def calculate_transfer_amount(self, btc_amount: float, provider: str,
                                 currency: str, btc_rate: float) -> Dict:
        """
        Calculate transfer amount after fees
        
        Args:
            btc_amount: Bitcoin amount
            provider: Mobile money provider
            currency: Target currency
            btc_rate: BTC to currency exchange rate
            
        Returns:
            dict: Transfer details including fees
        """
        if provider not in self.TRANSFER_FEES:
            raise ValueError(f"Unknown provider: {provider}")
        
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}")
        
        # Calculate fiat amount
        fiat_amount = btc_amount * btc_rate
        
        # Calculate fees
        fee_rate = self.TRANSFER_FEES[provider]
        fee_amount = fiat_amount * fee_rate
        
        # Net amount after fees
        net_amount = fiat_amount - fee_amount
        
        return {
            'btc_amount': btc_amount,
            'fiat_amount': round(fiat_amount, 2),
            'currency': currency,
            'provider': provider,
            'fee_rate': f"{fee_rate * 100}%",
            'fee_amount': round(fee_amount, 2),
            'net_amount': round(net_amount, 2),
            'btc_rate': btc_rate,
            'timestamp': datetime.now().isoformat()
        }
    
    def initiate_transfer(self, btc_amount: float, phone_number: str,
                         provider: str, currency: str, btc_rate: float,
                         user_id: str = None) -> Dict:
        """
        Initiate a mobile money transfer
        
        Args:
            btc_amount: Bitcoin amount to transfer
            phone_number: Recipient phone number
            provider: Mobile money provider
            currency: Target currency
            btc_rate: Current BTC to currency rate
            user_id: Optional user identifier
            
        Returns:
            dict: Transfer transaction details
        """
        # Validate inputs
        if not self._validate_phone_number(phone_number, provider, currency):
            return {'error': 'Invalid phone number for provider and country'}
        
        if provider not in self.TRANSFER_FEES:
            return {'error': f'Provider {provider} not supported'}
        
        if currency not in self.SUPPORTED_CURRENCIES:
            return {'error': f'Currency {currency} not supported'}
        
        # Calculate transfer details
        transfer_details = self.calculate_transfer_amount(btc_amount, provider, currency, btc_rate)
        
        # Check limits
        limits = self.LIMITS.get(provider, {})
        min_limit = limits.get('min', 0)
        max_limit = limits.get('max', 1000)
        
        if transfer_details['fiat_amount'] < min_limit:
            return {'error': f'Amount below minimum ({min_limit} {currency})'}
        
        if transfer_details['fiat_amount'] > max_limit:
            return {'error': f'Amount exceeds maximum ({max_limit} {currency})'}
        
        # Create transaction
        transaction = {
            'id': self._generate_transaction_id(),
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'btc_amount': btc_amount,
            'fiat_amount': transfer_details['fiat_amount'],
            'currency': currency,
            'provider': provider,
            'phone_number': self._mask_phone_number(phone_number),
            'fee_amount': transfer_details['fee_amount'],
            'net_amount': transfer_details['net_amount'],
            'status': 'pending',
            'confirmation_code': None,
            'reference': None
        }
        
        self.transaction_history.append(transaction)
        logger.info(f"Transfer initiated: {btc_amount} BTC to {provider} ({phone_number})")
        
        return {
            'success': True,
            'transaction_id': transaction['id'],
            'status': 'pending',
            'details': transfer_details,
            'message': f'Transfer initiated. Please confirm on your {provider} mobile wallet.'
        }
    
    def confirm_transfer(self, transaction_id: str, confirmation_code: str) -> Dict:
        """
        Confirm a mobile money transfer
        
        Args:
            transaction_id: Transaction ID
            confirmation_code: Confirmation code from mobile wallet
            
        Returns:
            dict: Confirmation result
        """
        transaction = None
        for tx in self.transaction_history:
            if tx['id'] == transaction_id:
                transaction = tx
                break
        
        if not transaction:
            return {'error': 'Transaction not found'}
        
        if transaction['status'] != 'pending':
            return {'error': f'Transaction already {transaction["status"]}'}
        
        # In a real implementation, this would verify with the provider's API
        transaction['status'] = 'confirmed'
        transaction['confirmation_code'] = confirmation_code
        transaction['reference'] = self._generate_reference_number()
        
        logger.info(f"Transfer confirmed: {transaction_id}")
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'status': 'confirmed',
            'reference': transaction['reference'],
            'message': 'Transfer confirmed. Funds will be deposited shortly.'
        }
    
    def get_transaction_status(self, transaction_id: str) -> Dict:
        """
        Get transaction status
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            dict: Transaction details and status
        """
        for transaction in self.transaction_history:
            if transaction['id'] == transaction_id:
                return transaction
        
        return {'error': 'Transaction not found'}
    
    def get_transfer_history(self, user_id: str = None, limit: int = 10) -> List[Dict]:
        """
        Get transfer history
        
        Args:
            user_id: Optional user filter
            limit: Number of records to return
            
        Returns:
            list: Transaction history
        """
        history = self.transaction_history
        
        if user_id:
            history = [tx for tx in history if tx.get('user_id') == user_id]
        
        return history[-limit:]
    
    def estimate_btc_amount_for_transfer(self, fiat_amount: float, provider: str,
                                        btc_rate: float) -> Dict:
        """
        Estimate BTC needed for a specific fiat amount
        
        Args:
            fiat_amount: Target fiat amount
            provider: Mobile money provider
            btc_rate: Current BTC to fiat rate
            
        Returns:
            dict: BTC amount needed
        """
        if provider not in self.TRANSFER_FEES:
            return {'error': f'Provider {provider} not supported'}
        
        fee_rate = self.TRANSFER_FEES[provider]
        
        # fiat_amount = btc_needed * btc_rate * (1 - fee_rate)
        # btc_needed = fiat_amount / (btc_rate * (1 - fee_rate))
        
        btc_needed = fiat_amount / (btc_rate * (1 - fee_rate))
        fees_in_btc = btc_needed * fee_rate
        
        return {
            'target_fiat_amount': fiat_amount,
            'btc_needed': round(btc_needed, 8),
            'fees_in_btc': round(fees_in_btc, 8),
            'provider': provider,
            'btc_rate': btc_rate
        }
    
    def get_provider_info(self, provider: str) -> Dict:
        """
        Get provider information
        
        Args:
            provider: Provider name
            
        Returns:
            dict: Provider details
        """
        if provider not in self.TRANSFER_FEES:
            return {'error': f'Provider {provider} not found'}
        
        limits = self.LIMITS.get(provider, {})
        fee_rate = self.TRANSFER_FEES[provider]
        
        # Find supported currencies
        supported_currencies = []
        for curr, info in self.SUPPORTED_CURRENCIES.items():
            if provider in info['providers']:
                supported_currencies.append(curr)
        
        return {
            'name': provider,
            'fee_rate': f"{fee_rate * 100}%",
            'min_amount': limits.get('min', 'N/A'),
            'max_amount': limits.get('max', 'N/A'),
            'supported_currencies': supported_currencies,
            'description': self._get_provider_description(provider)
        }
    
    @staticmethod
    def _validate_phone_number(phone_number: str, provider: str, currency: str) -> bool:
        """
        Validate phone number format for provider and currency
        
        Args:
            phone_number: Phone number to validate
            provider: Mobile money provider
            currency: Currency code
            
        Returns:
            bool: True if valid
        """
        # Remove common formatting
        phone = phone_number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # Validate by country/provider
        if currency == 'UGX':
            # Uganda: starts with +256 or 0
            return len(phone) >= 9 and (phone.startswith('256') or phone.startswith('0'))
        elif currency == 'KES':
            # Kenya: starts with +254 or 0
            return len(phone) >= 9 and (phone.startswith('254') or phone.startswith('0'))
        
        # Basic validation
        return len(phone) >= 9 and phone.isdigit()
    
    @staticmethod
    def _mask_phone_number(phone_number: str) -> str:
        """
        Mask phone number for privacy
        
        Args:
            phone_number: Phone number to mask
            
        Returns:
            str: Masked phone number
        """
        # Show only first 3 and last 2 digits
        if len(phone_number) < 5:
            return "***"
        return phone_number[:3] + "****" + phone_number[-2:]
    
    @staticmethod
    def _generate_transaction_id() -> str:
        """
        Generate unique transaction ID
        
        Returns:
            str: Transaction ID
        """
        import uuid
        return f"TX-{uuid.uuid4().hex[:12].upper()}"
    
    @staticmethod
    def _generate_reference_number() -> str:
        """
        Generate reference number for transfer
        
        Returns:
            str: Reference number
        """
        import uuid
        import time
        timestamp = int(time.time() * 1000) % 1000000
        return f"{timestamp}-{uuid.uuid4().hex[:8].upper()}"
    
    @staticmethod
    def _get_provider_description(provider: str) -> str:
        """
        Get provider description
        
        Args:
            provider: Provider name
            
        Returns:
            str: Provider description
        """
        descriptions = {
            'MTN': 'MTN Mobile Money - Available in Uganda, Ghana, Kenya, Nigeria, Cameroon',
            'AIRTEL': 'Airtel Money - Available in Uganda, Kenya, Tanzania, Nigeria',
            'UGANDA_TELECOM': 'Uganda Telecom Money - Available in Uganda',
            'ORANGE': 'Orange Money - Available in Egypt, Ivory Coast, Cameroon',
            'VODAFONE': 'Vodafone Cash - Available in Ghana, Egypt',
            'SAFARICOM': 'M-Pesa - Available in Kenya, Tanzania',
            'EQUITEL': 'Equitel - Available in Kenya',
        }
        return descriptions.get(provider, 'Unknown provider')
