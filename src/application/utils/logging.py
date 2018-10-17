import os
import logging.config

import yaml


def setup_logging(default_path='logging.yml',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """Setup logging configuration
    https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logging.debug('Loaded yml config.')
    else:
        logging.basicConfig(level=default_level)
        logging.debug('Loaded default config.')
