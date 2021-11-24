import logging


logger = logging
logger.basicConfig(filename='logs/tests.log',
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   level=logging.ERROR)

BASE = 'http://127.0.0.1:5000/'
