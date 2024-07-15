import asyncio
import config

import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

async def client_task(reader, writer):
    name = writer.get_extra_info('peername')
    while True:
        msg = (await reader.read(2048)).decode('utf-8')
        if len(msg) == 0:
            # continue
            logging.info(f'{name}: client disconnected')
            return
        else:
            logging.info(f'{name}: received message: {msg}')
            if msg == config.SERVER_DISCONNECT_MSG:
                logging.info(f'{name}: requested disconnect')
                return

def client_connected_cb(reader, writer):
    logging.info(f'{writer.get_extra_info('peername')}: client connected')
    asyncio.ensure_future(client_task(reader, writer))

loop = asyncio.get_event_loop()
server_coro = asyncio.start_server(client_connected_cb, host = config.BIND_HOST, port = config.PORT)
server = loop.run_until_complete(server_coro)

try:
    logging.info(f'server listening on {config.HOST}:{config.PORT}.')
    loop.run_forever()
finally:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()