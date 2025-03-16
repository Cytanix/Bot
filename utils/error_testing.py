import asyncio
from utils.error_reporting import send_error

async def test_error_reporting():
    error_name = "test_error"
    error_message = "This is a test error message."
    result = await send_error(error_name, error_message)
    print(result)


asyncio.run(test_error_reporting())
