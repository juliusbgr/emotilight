import asyncio
import os
from dotenv import load_dotenv
from govee_api_laggat import Govee, GoveeAbstractLearningStorage, GoveeLearnedInfo
from typing import Dict

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
        return "deep_relax", (255, 80, 80), 40     # soft, dim red
    elif stress_factor > 0.5:
        return "relax", (255, 220, 180), 50        # warm soft white
    elif stress_factor > 0.3:
        return "neutral", (255, 200, 150), 40      # gentle peach
    else:
        return "cool_rest", (180, 220, 255), 30    # cool light blue

import check_ins
async def main():
    # load_dotenv()
    # api_key = os.getenv("GOVEE_API_KEY")
    # if not api_key:
    #     print("API key missing.")
    #     return

    mood_stress = check_ins.main()
    calendar_stress = 0.8
    wearable_stress = None

    stress_factor = compute_stress_factor(calendar_stress, mood_stress, wearable_stress)
    light_state, rgb, brightness = get_light_state(stress_factor)
    
    print(f"Computed stress factor: {stress_factor:.2f}")
    print(f"Light state: {light_state}, RGB: {rgb}, Brightness: {brightness}%")

    # async with Govee(api_key=api_key, learning_storage=YourLearningStorage()) as govee:
    #     devices, err = await govee.get_devices()
    #     if err or not devices:
    #         print("Error getting devices:", err)
    #         return

    #     device = govee.device(devices[0].device)  # not just devices[0]!
    #     print(f"Setting {device} to '{light_state}' mode (stress: {stress_factor:.2f}, brightness: {brightness}%)")

    #     await govee.turn_on(device)
    #     await govee.set_color(device, rgb)
    #     await govee.set_brightness(device, brightness)

if __name__ == "__main__":
    asyncio.run(main())