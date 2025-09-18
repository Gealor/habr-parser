from pathlib import Path
from typing import Callable
import json

def write_into_file(filename: Path):
    def inner_func(func: Callable):
        async def wrapper(*args, **kwargs):
            result: dict = await func(*args, **kwargs)
            json_result = json.dumps(result, indent=4, ensure_ascii=False) # ensure_ascii для корректного вывода кириллицы
            print(json_result)
            with open(file=filename, mode="w", encoding="utf-8") as file:
                file.write(json_result)
            return result
        return wrapper
    return inner_func