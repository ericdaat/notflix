import os
import logging.config

import yaml


def setup_logging(log_dir,
                  config_path="logging.yml",
                  level=logging.DEBUG):
    """Setup logging configuration
    """
    if os.path.isfile(config_path):
        with open(config_path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logging.info("Loaded config from yml file.")
    else:
        logging.basicConfig(level=level)
        logging.info("Loaded default config.")

