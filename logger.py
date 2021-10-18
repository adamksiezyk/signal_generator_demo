import logging.config
import yaml
from datetime import datetime


def log(original_class: type) -> type:
    # Save original __init__
    original_init = original_class.__init__

    # Create logger
    with open('logger.yaml', 'r') as f:
        config_parsed = f.read().replace(
            "__TIMESTAMP__", datetime.now().strftime("%H-%M-%S_%d-%m-%Y"))
        config = yaml.safe_load(config_parsed)
        logging.config.dictConfig(config)
    logger = logging.getLogger(original_class.__name__)

    # Define new __init__
    def __init__(self, *args, **kwargs) -> None:
        original_init(self, logger, *args, **kwargs)

    # Override __init__
    original_class.__init__ = __init__
    return original_class
