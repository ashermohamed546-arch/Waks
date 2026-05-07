#!/usr/bin/env python3
"""
Bitcoin Miner - Main mining engine
Supports CPU mining, GPU mining, and pool mining
"""

import hashlib
import time
import threading
import json
import logging
from datetime import datetime
from multiprocessing import Pool, cpu_count
from .hash_engine import HashEngine
from .utils import format_hashrate, get_cpu_info

logger = logging.getLogger(__name__)


class BitcoinMiner:
    """Bitcoin mining engine with multiple modes"""
    
    def __init__(self, config, mode='cpu'):
        """
        Initialize the Bitcoin Miner
        
        Args:
            config (dict): Configuration dictionary
            mode (str): Mining mode - 'cpu', 'gpu', 'pool', 'hybrid'
        """
        self.config = config
        self.mode = mode
        self.hash_engine = HashEngine()
        
        # Mining statistics
        self.stats = {
            'total_hashes': 0,
            'valid_hashes': 0,
            'shares_accepted': 0,
            'shares_rejected': 0,
            'start_time': None,
            'uptime': 0,
            'average_hashrate': 0,
            'current_hashrate': 0,
            'difficulty': config['mining']['difficulty'],
            'blocks_found': 0,
            'last_block_time': None,
        }
        
        self.running = False
        self.threads = []
        self.lock = threading.Lock()
        
        logger.info(f"BitcoinMiner initialized in {mode} mode")
        logger.info(f"Threads: {config['mining']['threads']}")
        logger.info(f"Difficulty: {config['mining']['difficulty']}")
    
    def start(self):
        """Start the mining process"""
        self.running = True
        self.stats['start_time'] = datetime.now()
        
        logger.info(f"Starting {self.mode} mining...")
        logger.info(f"CPU Info: {get_cpu_info()}")
        
        if self.mode == 'cpu':
            self._start_cpu_mining()
        elif self.mode == 'gpu':
            self._start_gpu_mining()
        elif self.mode == 'pool':
            self._start_pool_mining()
        elif self.mode == 'hybrid':
            self._start_hybrid_mining()
    
    def _start_cpu_mining(self):
        """Start CPU mining with multiple threads"""
        num_threads = self.config['mining']['threads']
        
        logger.info(f"Starting CPU mining with {num_threads} threads")
        
        for thread_id in range(num_threads):
            t = threading.Thread(
                target=self._mine_cpu,
                args=(thread_id,),
                daemon=True,
                name=f"MinerThread-{thread_id}"
            )
            t.start()
            self.threads.append(t)
        
        # Monitor thread
        monitor = threading.Thread(
            target=self._monitor_mining,
            daemon=True,
            name="MonitorThread"
        )
        monitor.start()
        self.threads.append(monitor)
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    
    def _mine_cpu(self, thread_id):
        """CPU mining worker thread
        
        Args:
            thread_id (int): Thread identifier
        """
        logger.info(f"Mining thread {thread_id} started")
        
        nonce = 0
        target = self._calculate_target()
        last_stats = time.time()
        hashes_since_last = 0
        
        while self.running:
            try:
                # Create block data
                block_data = self._create_block_data(nonce)
                
                # Calculate hash
                block_hash = self.hash_engine.calculate_hash(block_data)
                
                with self.lock:
                    self.stats['total_hashes'] += 1
                    hashes_since_last += 1
                
                # Check if valid
                if self._is_valid_hash(block_hash):
                    with self.lock:
                        self.stats['valid_hashes'] += 1
                        self.stats['shares_accepted'] += 1
                        self.stats['blocks_found'] += 1
                        self.stats['last_block_time'] = datetime.now()
                    
                    logger.info(f"✓ Valid block found! Hash: {block_hash.hex()[:16]}...")
                    logger.info(f"  Nonce: {nonce}, Thread: {thread_id}")
                    logger.info(f"  Block #{self.stats['blocks_found']}")
                
                nonce += 1
                
                # Update stats periodically
                current_time = time.time()
                if current_time - last_stats >= 10:  # Every 10 seconds
                    with self.lock:
                        hashrate = hashes_since_last / (current_time - last_stats)
                        self.stats['current_hashrate'] = hashrate
                    hashes_since_last = 0
                    last_stats = current_time
                
                # Prevent nonce overflow
                if nonce > 2**32:
                    nonce = 0
                    
            except Exception as e:
                logger.error(f"Error in mining thread {thread_id}: {e}")
                time.sleep(1)
    
    def _start_gpu_mining(self):
        """Start GPU mining (placeholder for future implementation)"""
        logger.warning("GPU mining not yet implemented")
        logger.info("Falling back to CPU mining...")
        self._start_cpu_mining()
    
    def _start_pool_mining(self):
        """Start pool mining"""
        logger.info("Pool mining not yet fully implemented")
        logger.info("Starting in solo mode for now...")
        self._start_cpu_mining()
    
    def _start_hybrid_mining(self):
        """Start hybrid CPU + GPU mining"""
        logger.info("Hybrid mining - Starting CPU miners...")
        self._start_cpu_mining()
    
    def _monitor_mining(self):
        """Monitor mining progress and statistics"""
        last_total = 0
        last_time = time.time()
        
        while self.running:
            try:
                time.sleep(30)  # Update every 30 seconds
                
                current_time = time.time()
                elapsed = current_time - last_time
                
                with self.lock:
                    hashes_diff = self.stats['total_hashes'] - last_total
                    hashrate = hashes_diff / elapsed if elapsed > 0 else 0
                    
                    if self.stats['start_time']:
                        uptime = (current_time - self.stats['start_time'].timestamp())
                        self.stats['uptime'] = uptime
                        avg_hashrate = self.stats['total_hashes'] / uptime if uptime > 0 else 0
                        self.stats['average_hashrate'] = avg_hashrate
                    
                    # Log statistics
                    logger.info("\n" + "="*60)
                    logger.info("MINING STATISTICS")
                    logger.info("="*60)
                    logger.info(f"Current Hashrate:   {format_hashrate(hashrate)}")
                    logger.info(f"Average Hashrate:   {format_hashrate(self.stats['average_hashrate'])}")
                    logger.info(f"Total Hashes:       {self.stats['total_hashes']:,}")
                    logger.info(f"Valid Hashes:       {self.stats['valid_hashes']:,}")
                    logger.info(f"Shares Accepted:    {self.stats['shares_accepted']}")
                    logger.info(f"Shares Rejected:    {self.stats['shares_rejected']}")
                    logger.info(f"Blocks Found:       {self.stats['blocks_found']}")
                    logger.info(f"Uptime:             {self._format_uptime(self.stats['uptime'])}")
                    logger.info(f"Difficulty:         {self.stats['difficulty']}")
                    logger.info("="*60 + "\n")
                
                last_total = self.stats['total_hashes']
                last_time = current_time
                
            except Exception as e:
                logger.error(f"Error in monitor: {e}")
    
    def _create_block_data(self, nonce):
        """Create block data for mining
        
        Args:
            nonce (int): Nonce value
            
        Returns:
            bytes: Block data
        """
        block_data = {
            'timestamp': int(time.time()),
            'nonce': nonce,
            'difficulty': self.stats['difficulty'],
            'version': 1,
        }
        return json.dumps(block_data).encode()
    
    def _calculate_target(self):
        """Calculate mining target based on difficulty
        
        Returns:
            int: Target value
        """
        # Simplified target calculation
        # In real Bitcoin: target = max_target / difficulty
        return 2 ** (256 - self.stats['difficulty'])
    
    def _is_valid_hash(self, hash_value):
        """Check if hash meets difficulty requirement
        
        Args:
            hash_value (bytes): Hash to check
            
        Returns:
            bool: True if valid
        """
        # Check if hash starts with required number of zeros
        hash_int = int.from_bytes(hash_value, byteorder='big')
        target = self._calculate_target()
        return hash_int < target
    
    def _format_uptime(self, seconds):
        """Format uptime to human-readable format
        
        Args:
            seconds (float): Uptime in seconds
            
        Returns:
            str: Formatted uptime
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"
    
    def stop(self):
        """Stop the mining process"""
        logger.info("Stopping mining...")
        self.running = False
        
        # Wait for all threads
        for t in self.threads:
            if t.is_alive():
                t.join(timeout=2)
        
        # Final statistics
        with self.lock:
            if self.stats['start_time']:
                total_uptime = (datetime.now() - self.stats['start_time']).total_seconds()
                avg_rate = self.stats['total_hashes'] / total_uptime if total_uptime > 0 else 0
                
                logger.info("\n" + "="*60)
                logger.info("FINAL MINING REPORT")
                logger.info("="*60)
                logger.info(f"Total Runtime:      {self._format_uptime(total_uptime)}")
                logger.info(f"Average Hashrate:   {format_hashrate(avg_rate)}")
                logger.info(f"Total Hashes:       {self.stats['total_hashes']:,}")
                logger.info(f"Valid Hashes:       {self.stats['valid_hashes']:,}")
                logger.info(f"Blocks Found:       {self.stats['blocks_found']}")
                logger.info(f"Shares Accepted:    {self.stats['shares_accepted']}")
                logger.info(f"Acceptance Rate:    {(self.stats['shares_accepted'] / (self.stats['shares_accepted'] + self.stats['shares_rejected']) * 100) if (self.stats['shares_accepted'] + self.stats['shares_rejected']) > 0 else 0:.2f}%")
                logger.info("="*60)
    
    def get_stats(self):
        """Get current mining statistics
        
        Returns:
            dict: Statistics dictionary
        """
        with self.lock:
            return self.stats.copy()
