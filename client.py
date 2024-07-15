import socket
import config
import time
import random

import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((config.HOST, config.PORT))
logging.info(f'client connected to {config.HOST}:{config.PORT}')

n = 0
while config.CLIENT_MSG_CNT is None or n < config.CLIENT_MSG_CNT:
    data = f'{config.CLIENT_MSG} (#{n + 1}) - our random number for today is {random.randint(1, 100)}'
    logging.debug(f'sending to server: {data}')
    t_start = time.time()
    client.send(data.encode('utf-8'))
    t_end = time.time()
    logging.info(f'last message took {t_end - t_start} sec to send')
    time.sleep(config.CLIENT_MSG_ITVL)
    n += 1

logging.info(f'disconnecting from server')
client.send(config.SERVER_DISCONNECT_MSG.encode('utf-8'))
client.close()