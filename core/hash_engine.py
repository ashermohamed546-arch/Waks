#!/usr/bin/env python3
"""
Hash Engine - Cryptographic hash calculations
Supports SHA-256 (Bitcoin) and other algorithms
"""

import hashlib
import logging
from typing import Union

logger = logging.getLogger(__name__)


class HashEngine:
    """Cryptographic hash calculation engine"""
    
    # Hash algorithms
    SHA256 = 'sha256'
    SCRYPT = 'scrypt'
    SHA512 = 'sha512'
    BLAKE2B = 'blake2b'
    
    def __init__(self, algorithm=SHA256):
        """
        Initialize hash engine
        
        Args:
            algorithm (str): Hash algorithm to use
        """
        self.algorithm = algorithm
        logger.info(f"HashEngine initialized with {algorithm} algorithm")
    
    def calculate_hash(self, data: Union[bytes, str], algorithm: str = None) -> bytes:
        """
        Calculate hash of data
        
        Args:
            data: Data to hash (bytes or string)
            algorithm: Hash algorithm (uses default if None)
            
        Returns:
            bytes: Hash value
        """
        if algorithm is None:
            algorithm = self.algorithm
        
        if isinstance(data, str):
            data = data.encode()
        
        if algorithm == self.SHA256:
            return self._sha256(data)
        elif algorithm == self.SCRYPT:
            return self._scrypt(data)
        elif algorithm == self.SHA512:
            return self._sha512(data)
        elif algorithm == self.BLAKE2B:
            return self._blake2b(data)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    @staticmethod
    def _sha256(data: bytes) -> bytes:
        """
        SHA-256 hash (Bitcoin standard)
        
        Args:
            data: Data to hash
            
        Returns:
            bytes: SHA-256 hash
        """
        return hashlib.sha256(data).digest()
    
    @staticmethod
    def _double_sha256(data: bytes) -> bytes:
        """
        Double SHA-256 hash (Bitcoin standard)
        
        Args:
            data: Data to hash
            
        Returns:
            bytes: Double SHA-256 hash
        """
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()
    
    @staticmethod
    def _sha512(data: bytes) -> bytes:
        """
        SHA-512 hash
        
        Args:
            data: Data to hash
            
        Returns:
            bytes: SHA-512 hash
        """
        return hashlib.sha512(data).digest()
    
    @staticmethod
    def _blake2b(data: bytes) -> bytes:
        """
        BLAKE2b hash
        
        Args:
            data: Data to hash
            
        Returns:
            bytes: BLAKE2b hash
        """
        return hashlib.blake2b(data).digest()
    
    @staticmethod
    def _scrypt(data: bytes) -> bytes:
        """
        Scrypt hash (Litecoin compatible)
        Note: Requires scrypt library for actual implementation
        
        Args:
            data: Data to hash
            
        Returns:
            bytes: Scrypt hash
        """
        try:
            import scrypt
            return scrypt.hash(data, data, 32768, 8, 1, 32)
        except ImportError:
            logger.warning("scrypt library not installed, using SHA-256 instead")
            return hashlib.sha256(data).digest()
    
    def calculate_hash_hex(self, data: Union[bytes, str], algorithm: str = None) -> str:
        """
        Calculate hash and return as hexadecimal string
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm (uses default if None)
            
        Returns:
            str: Hash in hexadecimal format
        """
        hash_bytes = self.calculate_hash(data, algorithm)
        return hash_bytes.hex()
    
    def verify_hash(self, data: Union[bytes, str], hash_value: bytes, 
                   algorithm: str = None) -> bool:
        """
        Verify that data produces the given hash
        
        Args:
            data: Data to verify
            hash_value: Expected hash value
            algorithm: Hash algorithm (uses default if None)
            
        Returns:
            bool: True if hash matches
        """
        calculated = self.calculate_hash(data, algorithm)
        return calculated == hash_value
    
    def benchmark(self, iterations: int = 1000) -> dict:
        """
        Benchmark hash calculations
        
        Args:
            iterations: Number of iterations
            
        Returns:
            dict: Benchmark results
        """
        import time
        
        test_data = b"benchmark test data" * 100
        results = {}
        
        for algo in [self.SHA256, self.SHA512, self.BLAKE2B]:
            start = time.perf_counter()
            for _ in range(iterations):
                self.calculate_hash(test_data, algo)
            elapsed = time.perf_counter() - start
            
            rate = iterations / elapsed
            results[algo] = {
                'total_time': elapsed,
                'hash_rate': rate,
                'time_per_hash': elapsed / iterations
            }
        
        return results
