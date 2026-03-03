"""
Configuration management for the Autonomous Market Trend Identifier system.
Centralizes all configurable parameters with type safety and validation.
"""
import os
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import json
from pathlib import Path
import logging

class TradingInterval(str, Enum):
    MINUTE = "1m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    HOUR = "1h"
    FOUR_HOUR = "4h"
    DAY = "1d"

@dataclass
class TrendDetectionConfig:
    """Configuration for trend detection module"""
    # Clustering parameters
    n_clusters: int = 5
    max_clusters: int = 10
    min_samples_per_cluster: int = 20
    random_state: int = 42
    
    # Feature engineering
    feature_window_sizes: List[int] = None
    volatility_periods: List[int] = None
    rsi_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    
    # Validation
    min_trend_duration: int = 6  # Minimum candles for valid trend
    trend_confidence_threshold: float = 0.7
    
    def __post_init__(self):
        if self.feature_window_sizes is None:
            self.feature_window_sizes = [5, 10, 20, 50]
        if self.volatility_periods is None:
            self.volatility_periods = [5, 10, 20]

@dataclass
class GANConfig:
    """Configuration for GAN-based synthetic data generation"""
    # Architecture
    generator_layers: List[int] = None
    discriminator_layers: List[int] = None
    latent_dim: int = 100
    dropout_rate: float = 0.3
    
    # Training
    epochs: int = 1000
    batch_size: int = 32
    learning_rate: float = 0.0002
    beta_1: float = 0.5
    
    # Validation
    wasserstein_gp_weight: float = 10.0
    critic_iterations: int = 5
    
    def __post_init__(self):
        if self.generator_layers is None:
            self.generator_layers = [256, 512, 1024]
        if self.discriminator_layers is None:
            self.discriminator_layers = [1024, 512, 256]

@dataclass
class RLConfig:
    """Configuration for reinforcement learning strategy testing"""
    # Environment
    initial_balance: float = 10000.0
    transaction_cost: float = 0.001  # 0.1%
    max_position_size: float = 0.1  # 10% of portfolio
    episode_length: int = 1000
    
    # Algorithm (PPO)
    learning_rate: float = 3e-4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_epsilon: float = 0.2
    entropy_coef: float = 0.01
    
    # Training
    n_envs: int = 4
    n_steps: int = 2048
    batch_size: int = 64
    n_epochs: int = 10

@dataclass
class DeploymentConfig:
    """Configuration for strategy deployment"""
    min_backtest_period: int = 30  # days
    min_sharpe_ratio: float = 1.5
    max_drawdown_threshold: float = 0.25  # 25%
    min_profit_factor: float = 1.3
    deployment_batch_size: int = 5
    cooling_period: int = 24  # hours between deployments

@dataclass
class SystemConfig:
    """Main system configuration"""
    # Firebase
    firestore_collections: Dict[str, str] = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Data
    data_cache_duration: int = 3600  # seconds
    max_data_points: int = 10000
    
    # Monitoring
    health_check_interval: int = 300  # seconds
    performance_report_interval: int = 3600  # seconds
    
    def __post_init__(self):
        if self.firestore_collections is None:
            self.firestore_collections = {
                "market_data": "market_data",
                "detected_trends": "detected_trends",
                "synthetic_data": "synthetic_data",
                "strategies": "trading_strategies",
                "deployments": "strategy_deployments",
                "performance": "performance_metrics"
            }
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        config =