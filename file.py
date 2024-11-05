import json
import aiofiles


async def read_json(filename: str = 'file_service.json'):
    async with aiofiles.open(filename, mode='r', encoding='UTF-8') as f:
        file_content = await f.read()
        return json.loads(file_content)