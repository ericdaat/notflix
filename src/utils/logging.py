import os
import logging.config
import yaml


def setup_logging(config_path):
    """Setup logging configuration
    """
    if os.path.isfile(config_path):
        with open(config_path, "rt") as f:
            config = yaml.safe_load(f.read())

        for handler_name, handler_conf in config["handlers"].items():
            if "filename" not in handler_conf.keys():
                continue

            log_path = os.path.dirname(handler_conf["filename"])

            if not os.path.exists(log_path):
                os.mkdir(log_path)

        logging.config.dictConfig(config)
        logging.info("Loaded config from yml file.")
    else:
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Loaded default config.")
