from config import LOGGER_ID

async def send_log(client, text: str):
    if LOGGER_ID:
        try:
            await client.send_message(LOGGER_ID, text)
        except Exception as e:
            print(f"Failed to send log: {e}")
