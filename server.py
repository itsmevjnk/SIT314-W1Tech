import socket
import config

import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((config.HOST, config.PORT))
server.listen(5)

logging.info(f'server listening on {config.HOST}:{config.PORT}.')

# connection handler
class ConnHandler:
    def __init__(self, conn: socket.socket):
        self.conn = conn
        self.name = str(conn.getsockname())
        logging.info(f'{self.name}: new connection')

    def __del__(self):
        logging.info(f'{self.name}: destroying object')
        self.conn.close() # close connection - the handler will exit by itself (hopefully)

    def run(self):
        self.handler_thread = threading.Thread(target=self.handler)
        self.handler_thread.run()

    def handler(self):
        while True:
            msg = self.conn.recv(2048).decode('utf-8')
            if len(msg) == 0:
                logging.info(f'{self.name}: client disconnected')
                return
            else:
                logging.debug(f'{self.name}: received message: {msg}')
                if msg == config.SERVER_DISCONNECT_MSG:
                    logging.info(f'{self.name}: requested disconnect')
                    self.conn.close()
                    return

# loop for dispatching connection handler threads
handlers = []
def conn_loop():
    while True:
        conn, addr = server.accept() # wait until new client arrives
        handlers.append(ConnHandler(conn))
        handlers[-1].run()
threading.Thread(target=conn_loop).run() # launch loop in a different thread so we can listen for Ctrl-C

try:
    while True: pass
finally:
    for h in handlers:
        del h
