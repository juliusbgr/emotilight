import asyncio
from govee_api_laggat import Govee
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOVEE_API_KEY")

def compute_stress_factor(calendar_stress, mood_score, wearable_stress):
    # Ensure inputs are between 0 and 1
    for val in [calendar_stress, mood_score, wearable_stress]:
        if not (0.0 <= val <= 1.0):
            raise ValueError("All input values must be between 0 and 1.")
    
    return (calendar_stress + mood_score + wearable_stress) / 3


def get_light_state(stress_factor):
    if stress_factor > 0.7:
        return "alarm", (255, 0, 0), 100      # red + brightness 100%
    elif stress_factor > 0.5:
        return "focus", (255, 255, 255), 80  # white + brightness 80%
    elif stress_factor > 0.3:
        return "calm", (255, 165, 0), 60     # orange + brightness 60%
    else:
        return "rest", (0, 0, 255), 30       # blue + brightness 30%


async def main(): #async function so that program is not blocked while waiting for the API response
    # example inputs
    calendar_stress = 0.7 # already normalized from other code
    mood_score = 0.8 #already normalized from other code
    wearable_input = 0.8 #already normalized from other code

    stress_factor = compute_stress_factor(calendar_stress, mood_score, wearable_input)
    light_state, rgb, brightness = get_light_state(stress_factor)

    govee = Govee(api_key=API_KEY)
    devices = await govee.get_devices()

    if not devices:
        print("No device found.")
        return

    device = devices[0]
    print(f"Setting {device.device_name} to '{light_state}' mode (stress: {stress_factor:.2f})"
          f"(stress: {stress_factor:.2f}, brightness: {brightness}%)")
    await govee.turn_on(device)
    await govee.set_color(device, *rgb)  #light color based on stress factor
    await govee.set_brightness(device, brightness)

if __name__ == "__main__":
    asyncio.run(main())

# run python test_govee.py in terminal (need venv, bulb needs to be on and connected to the same network -> mobile hotspot)