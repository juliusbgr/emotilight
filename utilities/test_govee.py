import asyncio
from govee_api_laggat import Govee
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOVEE_API_KEY")

async def main(): #async function so that program is not blocked while waiting for the API response
    govee = Govee(api_key=API_KEY)
    devices = await govee.get_devices()

    if not devices:
        print("No device found.")
        return

    device = devices[0]
    print(f"Control device: {device.device_name}")
    await govee.turn_on(device)
    await govee.set_color(device, 255, 0, 0)  #red

if __name__ == "__main__":
    asyncio.run(main())

# run python test_govee.py in terminal (bulb needs to be on and connected to the same network -> mobile hotspot)