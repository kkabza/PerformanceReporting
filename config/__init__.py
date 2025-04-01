"""
Configuration loader for the Performance Reporting application.
Loads the appropriate configuration based on the environment.
"""
import os
import logging

# Import all configs
from config.base import BaseConfig
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

def get_config():
    """
    Load and return the appropriate configuration based on the FLASK_ENV
    environment variable.
    
    Returns:
        Config class: The configuration class for the current environment.
    """
    env = os.getenv('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    selected_config = config_map.get(env, DevelopmentConfig)
    logging.info(f"Loading {env} configuration")
    
    return selected_config 