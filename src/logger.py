# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime


def get_logger(name: str = 'veri_pipeline') -> logging.Logger:
    """
    Hem konsola hem logs/ klasorune yazan logger dondurur.
    """
    logger = logging.getLogger(name)
    if logger.handlers:          # Ayni logger tekrar cagrilirsa duplicate handler olmasin
        return logger

    logger.setLevel(logging.DEBUG)

    # Log klasorunu olustur
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    tarih = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dosyasi = os.path.join(log_dir, f'pipeline_{tarih}.log')

    fmt = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Dosyaya yaz
    fh = logging.FileHandler(log_dosyasi, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # Konsola yaz
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger