import asyncio
import os

from file import read_json
from worker import parser_worker

from dotenv import load_dotenv


async def main(worker_data, host = None, port = None, login = None, password = None):
    queue = asyncio.Queue()
    for index_block_parser in worker_data:
        await queue.put((host, port, login, password, worker_data[index_block_parser]))

    workers = [asyncio.create_task(parser_worker(queue=queue)) for _ in range(3)]

    await queue.join()

    for worker in workers:
        worker.cancel()

if __name__ == "__main__":
    load_dotenv()

    host = os.getenv("HOST")
    port = os.getenv("PORT")
    login = os.getenv("USER")
    password = os.getenv("PASSWORD")

    worker_data = read_json("test.json")

    asyncio.run(main(host=host, port=port, login=login, password=password, worker_data=worker_data))