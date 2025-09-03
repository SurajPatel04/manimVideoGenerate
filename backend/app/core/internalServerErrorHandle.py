import asyncio
from google.api_core.exceptions import InternalServerError


async def retry(agent_executor, human_message, retries=3, delay=1):
    for attempt in range(retries):
        try:
            return await agent_executor.ainvoke({"input": human_message})
        except InternalServerError as e:
            if attempt < retries - 1:
                wait_time =  delay * (2 ** attempt)
                print(f"Internal error ({e}), retrying in {wait_time}s... (attempt {attempt+1})")
                await asyncio.sleep(wait_time)
            else:
                print(f"Max retries reached. Raising error.")
                raise