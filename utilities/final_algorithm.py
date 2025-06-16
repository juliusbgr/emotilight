import asyncio
from govee_api_laggat import Govee
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOVEE_API_KEY")

def compute_stress_factor(calendar_stress=None, mood_stress=None, wearable_stress=None):
    inputs = [calendar_stress, mood_stress, wearable_stress]
    valid_inputs = [i for i in inputs if i is not None]

    if not valid_inputs:
        raise ValueError("At least one input is required to compute stress.")

    # all inputs are already normalized to 0..1 from previous algorithms
    weight = 1 / len(valid_inputs)
    stress_factor = sum(i * weight for i in valid_inputs)

    return stress_factor



def get_light_state(stress_factor):
    if stress_factor > 0.7:
        return "alarm", (255, 0, 0), 100      # red + brightness 100%
    elif stress_factor > 0.5:
        return "focus", (255, 255, 255), 80  # white + brightness 80%
    elif stress_factor > 0.3:
        return "calm", (255, 165, 0), 60     # orange + brightness 60%
    else:
        return "rest", (0, 0, 255), 30       # blue + brightness 30%


async def main():
    # example inputs - any of these can be None
    calendar_stress = 0.7        # already normalized
    mood_stress = 0.8            # already normalized
    wearable_stress = None       # simulate missing input

    # automatically adjusts weights if any inputs are missing
    stress_factor = compute_stress_factor(
        calendar_stress=calendar_stress,
        mood_stress=mood_stress,
        wearable_stress=wearable_stress
    )

    light_state, rgb, brightness = get_light_state(stress_factor)

    govee = Govee(api_key=API_KEY)
    devices = await govee.get_devices()

    if not devices:
        print("No Govee device found.")
        return

    device = devices[0]
    print(f"Setting {device} to '{light_state}' mode "
          f"(stress: {stress_factor:.2f}, brightness: {brightness}%)")
    
    await govee.turn_on(device)
    await govee.set_color(device, *rgb)
    await govee.set_brightness(device, brightness)


if __name__ == "__main__":
    asyncio.run(main())

# run python test_govee.py in terminal (need venv, bulb needs to be on and connected to the same network -> mobile hotspot)