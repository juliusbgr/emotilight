import asyncio
import os
from dotenv import load_dotenv
from govee_api_laggat import Govee, GoveeAbstractLearningStorage, GoveeLearnedInfo
from typing import Dict


class YourLearningStorage(GoveeAbstractLearningStorage):
    async def read(self) -> Dict[str, GoveeLearnedInfo]:
        return {}

    async def write(self, learned_info: Dict[str, GoveeLearnedInfo]):
        pass


async def main():
    load_dotenv()
    api_key = os.getenv("GOVEE_API_KEY")
    if not api_key:
        print("API key missing. Set GOVEE_API_KEY in .env.")
        return

    async with Govee(api_key, learning_storage=YourLearningStorage()) as govee:
        devices, err = await govee.get_devices()
        if err or not devices:
            print("No devices found or API error:", err)
            return

        device = govee.device(devices[0].device)
        print(device)
        await govee.turn_on(device)
        await govee.set_color(device, (255, 0, 0))  # red


if __name__ == "__main__":
    asyncio.run(main())


# run python test_govee.py in terminal (bulb needs to be on and connected to the same network -> mobile hotspot)