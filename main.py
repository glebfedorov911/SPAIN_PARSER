import asyncio
import os

from file import read_json
from worker import parser_worker

from dotenv import load_dotenv


async def main(worker_data, host = None, port = None, login = None, password = None, client_cerf=None, client_key=None):
    queue = asyncio.Queue()
    for index_block_parser in worker_data:
        await queue.put((host, port, login, password, worker_data[index_block_parser]))

    workers = [asyncio.create_task(parser_worker(queue=queue)) for _ in range(3)]

    await queue.join()

    for worker in workers:
        worker.cancel()

if __name__ == "__main__":
    # host = "50.114.181.135"
    # port = 63120
    # login = "ZcTq1NqyS"
    # password = "aaczYwsJU"
    
    load_dotenv()

    host = "p1.mangoproxy.com"
    port = 2334
    login = "n66063054a6f17c192a006d-zone-custom-region-es"
    password = "b151e67bc2b9462683bdab5eb1ff4acc"

    worker_data = read_json("test.json")
    asyncio.run(main(host=host, port=port, login=login, password=password, worker_data=worker_data, 
    client_cerf=os.getenv("CLIENT_CERF"), client_key=os.getenv("CLIENT_KEY")))