import asyncio
import os
from dotenv import load_dotenv
from govee_api_laggat import Govee, GoveeAbstractLearningStorage, GoveeLearnedInfo
from typing import Dict
import colorsys

def hsbk_to_rgb_brightness(hue, saturation, brightness):
    """Convert HSB to RGB and return RGB (0–255) and brightness (0–100)"""
    r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, brightness)
    rgb = tuple(int(c * 255) for c in (r, g, b))
    brightness_pct = int(brightness * 100)
    return rgb, brightness_pct

class YourLearningStorage(GoveeAbstractLearningStorage):
    async def read(self) -> Dict[str, GoveeLearnedInfo]:
        return {}

    async def write(self, learned_info: Dict[str, GoveeLearnedInfo]):
        pass


modes_data = [
    {
        "Mode": "Calm",
        "Hex": "#AEDFF7",
        "HSBK": (200, 0.30, 0.70, 3000),
        "Transition (ms)": 3000,
        "Use Case / Rationale": "Soft sky-blue for low-arousal relaxation."
    },
    {
        "Mode": "Neutral",
        "Hex": "#FFF5B1",
        "HSBK": (55, 0.20, 0.80, 4000),
        "Transition (ms)": 1500,
        "Use Case / Rationale": "Gentle yellow for general tasks."
    },
    {
        "Mode": "Stress Relief",
        "Hex": "#88E1A3",
        "HSBK": (140, 0.45, 0.60, 3500),
        "Transition (ms)": 2000,
        "Use Case / Rationale": "Restorative green for calming."
    },
    {
        "Mode": "Panic",
        "Hex": "#FFA07A",
        "HSBK": (17, 0.50, 0.50, 2700),
        "Transition (ms)": 1000,
        "Use Case / Rationale": "Red-orange for grounding during high stress."
    }
]

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
        
        # Choose a mode (e.g., Calm)
        selected_mode = next((mode for mode in modes_data if mode["Mode"] == "Calm"), None)
        if not selected_mode:
            print("Selected mode not found.")
            return

        hue, saturation, brightness, kelvin = selected_mode["HSBK"]
        rgb, brightness_pct = hsbk_to_rgb_brightness(hue, saturation, brightness)

        print(f"Setting mode: {selected_mode['Mode']} -> RGB: {rgb}, Brightness: {brightness_pct}%")

        await govee.turn_on(device)
        await govee.set_color(device, rgb)
        await govee.set_brightness(device, brightness_pct)

        # Optional: simulate transition delay
        await asyncio.sleep(selected_mode["Transition (ms)"] / 1000)


if __name__ == "__main__":
    asyncio.run(main())


# run python test_govee.py in terminal (bulb needs to be on and connected to the same network -> mobile hotspot)