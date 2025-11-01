import logging, os
from .calculator_config import cfg

def get_logger(name="calculator"):
    os.makedirs(cfg.LOG_DIR, exist_ok=True)
    log_path = os.path.join(cfg.LOG_DIR, "app.log")
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path, encoding="utf-8")
        sh = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        fh.setFormatter(fmt); sh.setFormatter(fmt)
        logger.addHandler(fh); logger.addHandler(sh)
    return logger
