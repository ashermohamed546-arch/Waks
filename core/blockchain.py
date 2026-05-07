#!/usr/bin/env python3
"""
Blockchain Utilities - Bitcoin blockchain operations
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class Block:
    """Represents a Bitcoin block"""
    
    def __init__(self, block_number: int, timestamp: int, data: str, 
                 previous_hash: str, nonce: int = 0):
        """
        Initialize a block
        
        Args:
            block_number: Block index number
            timestamp: Block creation timestamp
            data: Block data/transactions
            previous_hash: Hash of previous block
            nonce: Nonce value for mining
        """
        self.block_number = block_number
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = None
    
    def calculate_hash(self) -> str:
        """
        Calculate block hash
        
        Returns:
            str: Block hash in hexadecimal
        """
        block_string = json.dumps({
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        
        hash_value = hashlib.sha256(block_string.encode()).hexdigest()
        self.hash = hash_value
        return hash_value
    
    def to_dict(self) -> dict:
        """
        Convert block to dictionary
        
        Returns:
            dict: Block as dictionary
        """
        return {
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Bitcoin blockchain implementation"""
    
    def __init__(self, difficulty: int = 4):
        """
        Initialize blockchain
        
        Args:
            difficulty: Mining difficulty level
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 50  # BTC
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """
        Create the genesis (first) block
        """
        genesis_block = Block(0, int(time.time()), "Genesis Block", "0")
        genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        logger.info("Genesis block created")
    
    def get_latest_block(self) -> Block:
        """
        Get the latest block in the chain
        
        Returns:
            Block: Latest block
        """
        return self.chain[-1]
    
    def add_transaction(self, sender: str, receiver: str, amount: float) -> bool:
        """
        Add a transaction to pending transactions
        
        Args:
            sender: Transaction sender
            receiver: Transaction receiver
            amount: Transaction amount
            
        Returns:
            bool: True if transaction added
        """
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
        self.pending_transactions.append(transaction)
        logger.info(f"Transaction added: {sender} -> {receiver}: {amount} BTC")
        return True
    
    def mine_block(self, miner_address: str) -> Optional[Block]:
        """
        Mine a new block
        
        Args:
            miner_address: Address of mining reward recipient
            
        Returns:
            Block: Newly mined block or None if failed
        """
        # Add mining reward transaction
        self.add_transaction("System", miner_address, self.mining_reward)
        
        # Create new block
        latest_block = self.get_latest_block()
        new_block = Block(
            block_number=len(self.chain),
            timestamp=int(time.time()),
            data=json.dumps(self.pending_transactions),
            previous_hash=latest_block.hash
        )
        
        # Mine the block
        while not new_block.calculate_hash().startswith('0' * self.difficulty):
            new_block.nonce += 1
        
        self.chain.append(new_block)
        self.pending_transactions = []
        
        logger.info(f"Block #{new_block.block_number} mined!")
        logger.info(f"Hash: {new_block.hash}")
        logger.info(f"Nonce: {new_block.nonce}")
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain
        
        Returns:
            bool: True if chain is valid
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check current block hash
            if current_block.hash != current_block.calculate_hash():
                logger.error(f"Invalid hash at block {i}")
                return False
            
            # Check previous hash reference
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"Invalid previous hash at block {i}")
                return False
            
            # Check difficulty
            if not current_block.hash.startswith('0' * self.difficulty):
                logger.error(f"Invalid difficulty at block {i}")
                return False
        
        logger.info("Blockchain is valid")
        return True
    
    def get_balance(self, address: str) -> float:
        """
        Get balance for an address
        
        Args:
            address: Bitcoin address
            
        Returns:
            float: Account balance
        """
        balance = 0
        
        for block in self.chain:
            if block.data == "Genesis Block":
                continue
            
            try:
                transactions = json.loads(block.data)
                for tx in transactions:
                    if tx['sender'] == address:
                        balance -= tx['amount']
                    if tx['receiver'] == address:
                        balance += tx['amount']
            except:
                pass
        
        return balance
    
    def get_chain_info(self) -> dict:
        """
        Get blockchain information
        
        Returns:
            dict: Blockchain info
        """
        return {
            'total_blocks': len(self.chain),
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward,
            'pending_transactions': len(self.pending_transactions),
            'is_valid': self.is_chain_valid(),
            'latest_block': self.get_latest_block().to_dict() if self.chain else None
        }


class BlockchainUtils:
    """Utility functions for blockchain operations"""
    
    @staticmethod
    def calculate_difficulty_from_hashrate(hashrate: float, 
                                          target_time: float = 600) -> int:
        """
        Calculate difficulty from hashrate
        
        Args:
            hashrate: Hashes per second
            target_time: Target block time in seconds
            
        Returns:
            int: Difficulty level
        """
        if hashrate <= 0:
            return 1
        return max(1, int(hashrate * target_time / (2 ** 32)))
    
    @staticmethod
    def estimate_blocks_to_mine(hashrate: float, difficulty: int) -> float:
        """
        Estimate time to mine a block
        
        Args:
            hashrate: Hashes per second
            difficulty: Mining difficulty
            
        Returns:
            float: Estimated time in seconds
        """
        if hashrate <= 0:
            return float('inf')
        
        target = 2 ** (256 - difficulty)
        expected_hashes = 2 ** 256 / target
        
        return expected_hashes / hashrate
