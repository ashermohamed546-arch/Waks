#!/usr/bin/env python3
"""
Utility functions for the mining engine
"""

import platform
import psutil
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def format_hashrate(hashrate: float) -> str:
    """
    Format hashrate to human-readable format
    
    Args:
        hashrate: Hashes per second
        
    Returns:
        str: Formatted hashrate
    """
    units = ['H/s', 'KH/s', 'MH/s', 'GH/s', 'TH/s', 'PH/s']
    
    for unit in units:
        if hashrate < 1000:
            return f"{hashrate:.2f} {unit}"
        hashrate /= 1000
    
    return f"{hashrate:.2f} EH/s"


def get_cpu_info() -> str:
    """
    Get CPU information
    
    Returns:
        str: CPU information
    """
    try:
        cpu_count = psutil.cpu_count(logical=False) or 1
        cpu_threads = psutil.cpu_count(logical=True) or 1
        cpu_freq = psutil.cpu_freq()
        cpu_model = platform.processor() or "Unknown"
        
        info = f"{cpu_model} ({cpu_count} cores, {cpu_threads} threads)"
        if cpu_freq:
            info += f" @ {cpu_freq.current:.2f} MHz"
        
        return info
    except Exception as e:
        logger.warning(f"Could not get CPU info: {e}")
        return "Unknown CPU"


def get_system_info() -> Dict[str, Any]:
    """
    Get system information
    
    Returns:
        dict: System information
    """
    try:
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'cpu_count': psutil.cpu_count(logical=True),
            'cpu_model': platform.processor(),
            'ram_total': psutil.virtual_memory().total,
            'ram_available': psutil.virtual_memory().available,
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {}


def show_system_info():
    """
    Display system information
    """
    info = get_system_info()
    
    print("\n" + "="*60)
    print("SYSTEM INFORMATION")
    print("="*60)
    print(f"Platform:           {info.get('platform')} {info.get('platform_release')}")
    print(f"CPU:                {get_cpu_info()}")
    print(f"RAM Total:          {info.get('ram_total') / (1024**3):.2f} GB")
    print(f"RAM Available:      {info.get('ram_available') / (1024**3):.2f} GB")
    print(f"CPU Usage:          {info.get('cpu_percent'):.1f}%")
    print(f"Memory Usage:       {info.get('memory_percent'):.1f}%")
    print("="*60 + "\n")


def estimate_mining_power(threads: int = None) -> float:
    """
    Estimate mining power in MH/s
    
    Args:
        threads: Number of threads (uses CPU count if None)
        
    Returns:
        float: Estimated hashrate in MH/s
    """
    if threads is None:
        threads = psutil.cpu_count(logical=True) or 1
    
    # Rough estimate: ~10 MH/s per thread
    # This varies greatly based on CPU and algorithm
    return threads * 10.0


def get_memory_usage() -> Dict[str, float]:
    """
    Get current memory usage
    
    Returns:
        dict: Memory usage statistics
    """
    try:
        vm = psutil.virtual_memory()
        return {
            'total': vm.total / (1024**3),  # GB
            'available': vm.available / (1024**3),
            'used': vm.used / (1024**3),
            'percent': vm.percent
        }
    except Exception as e:
        logger.error(f"Error getting memory usage: {e}")
        return {}
