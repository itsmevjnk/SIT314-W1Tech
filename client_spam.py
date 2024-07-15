import subprocess
import time

import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

clients = 0
while True:
    subprocess.Popen(['python', 'client.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    clients += 1
    logging.info(f'number of clients launched: {clients}')
    time.sleep(1) # 1 extra client every second
