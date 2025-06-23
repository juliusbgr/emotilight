import asyncio
import os
from dotenv import load_dotenv
from govee_api_laggat import Govee, GoveeAbstractLearningStorage, GoveeLearnedInfo
from typing import Dict
import re
import colorsys

modes_data = [
    {
        "Mode": "cool_rest",
        "Hex": "#AEDFF7",
        "HSBK": (200, 0.30, 0.70, 3000),
        "Transition (ms)": 3000,
        "Use Case / Rationale": "Soft sky-blue for low-arousal relaxation.",
        "Questions": "How much are you enjoying the present moment?"
    },
    {
        "Mode": "neutral",
        "Hex": "#FFF5B1",
        "HSBK": (55, 0.20, 0.80, 4000),
        "Transition (ms)": 1500,
        "Use Case / Rationale": "Gentle yellow for general tasks—uplifting without overstimulation.",
        "Questions": "How emotionally unsettled do you feel?"
    },
    {
        "Mode": "relax",
        "Hex": "#88E1A3",
        "HSBK": (140, 0.45, 0.60, 3500),
        "Transition (ms)": 2000,
        "Use Case / Rationale": "Restorative green to shift toward parasympathetic relaxation after stress."
    },
    {
        "Mode": "deep_relax",
        "Hex": "#FFA07A",
        "HSBK": (17, 0.50, 0.50, 2700),
        "Transition (ms)": 1000,
        "Use Case / Rationale": "Salmon-red pulsing to guide breathing and reduce acute stress."
    }
]

# Convert HSBK to RGB and brightness (0–100)
def hsbk_to_rgb_brightness(hue, saturation, brightness):
    r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, brightness)
    rgb = tuple(int(c * 255) for c in (r, g, b))
    brightness_pct = int(brightness * 100)
    return rgb, brightness_pct

# Dummy learning storage / can be used to store learned information for automation later on
class YourLearningStorage(GoveeAbstractLearningStorage):
    async def read(self) -> Dict[str, GoveeLearnedInfo]:
        return {}

    async def write(self, learned_info: Dict[str, GoveeLearnedInfo]):
        pass

def compute_stress_factor(calendar_stress=None, mood_stress=None, wearable_stress=None):
    inputs = [calendar_stress, mood_stress, wearable_stress]
    valid_inputs = [i for i in inputs if i is not None]
    if not valid_inputs:
        raise ValueError("At least one input is required to compute stress.")
    weight = 1 / len(valid_inputs)
    return sum(i * weight for i in valid_inputs)

def get_light_state(stress_factor):
    if stress_factor > 0.7:
        mode_name = "deep_relax"
    elif stress_factor > 0.5:
        mode_name = "relax"
    elif stress_factor > 0.3:
        mode_name = "neutral"
    else:
        mode_name = "cool_rest"

    mode = next((m for m in modes_data if m["Mode"] == mode_name), None)
    if not mode:
        raise ValueError(f"Mode '{mode_name}' not found in modes_data.")

    hue, saturation, brightness, kelvin = mode["HSBK"]
    rgb, brightness_pct = hsbk_to_rgb_brightness(hue, saturation, brightness)

    return mode_name, rgb, brightness_pct

import mood_check_ins
import heart_rate
import calendar_events

async def main():
    load_dotenv()
    api_key = os.getenv("GOVEE_API_KEY")
    if not api_key:
        print("API key missing.")
        return

    mood_stress = mood_check_ins.calculate_survey_score()
    
    while True:
        user_time = input("Enter a time (hh:mm): ")
        if re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", user_time):
            break
        print("Invalid format. Please enter time as hh:mm (e.g., 14:30).")
        
    calendar_stress = calendar_events.get_calendar_stress_score(user_time)
    wearable_stress = heart_rate.get_wearable_stress_score(user_time)

    stress_factor = compute_stress_factor(calendar_stress, mood_stress, wearable_stress)
    light_state, rgb, brightness = get_light_state(stress_factor)
    
    print(f"Computed stress factor: {stress_factor:.2f}")
    print(f"Light state: {light_state}, RGB: {rgb}, Brightness: {brightness}%")

    async with Govee(api_key=api_key, learning_storage=YourLearningStorage()) as govee:
        devices, err = await govee.get_devices()
        if err or not devices:
            print("Error getting devices:", err)
            return

        device = govee.device(devices[0].device)  # not just devices[0]!
        print(f"Setting {device} to '{light_state}' mode (stress: {stress_factor:.2f}, brightness: {brightness}%)")

        await govee.turn_on(device)
        await govee.set_color(device, rgb)
        await govee.set_brightness(device, brightness)

if __name__ == "__main__":
    asyncio.run(main())