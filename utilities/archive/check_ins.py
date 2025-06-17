# Ensure required packages are installed before running the script.
# Run the following command in your terminal:
# pip install govee-api-laggat python-dotenv

import asyncio
from govee_api_laggat import Govee
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOVEE_API_KEY")

# check-in questions
questions = [
    "How much is your mind racing right now? (1–10): ",
    "How anxious or stressed are you feeling right now? (1–10): ",
    "How emotionally unsettled do you feel? (1–10): ",
    "How out of control do your emotions feel right now? (1–10): "
]

# RGB presets for the final four moods
COLOR_MAP = {
    "Deep Rest":     (168, 218, 220),   # pale teal
    "Calm":          (174, 223, 247),   # soft sky-blue
    "Stress Relief": (136, 225, 163),   # restorative green
    "Panic":         (255,  69,   0)    # salmon-red
}

def get_user_scores():
    scores = []
    for q in questions:
        while True:
            try:
                val = int(input(q).strip())
                if 1 <= val <= 10:
                    scores.append(val)
                    break
                else:
                    print(" Please enter a number between 1 and 10.")
            except ValueError:
                print(" Invalid input. Enter an integer 1–10.")
    return scores

def compute_normalized_score(scores):
    total = sum(scores)
    normalized = total / (len(scores) * 10)  # max total = 4×10 = 40
    print(f"\nTotal score: {total}/40   Normalized: {normalized:.2f}")
    return normalized

def select_mood(normalized):
    if normalized <= 0.25:
        return "Deep Rest"
    elif normalized <= 0.50:
        return "Calm"
    elif normalized <= 0.75:
        return "Stress Relief"
    else:
        return "Panic"

# Temporarily commented out the async Govee control code. We do not need it here

# async def main(color: tuple[int,int,int]):
#     govee = Govee(api_key=API_KEY)
#     devices = await govee.get_devices()
#     if not devices:
#         print(" No Govee device found.")
#         return
#     device = devices[0]
#     print(f" Controlling device: {device.device_name} ({device.device})")

#     # Turn on and set color
#     await govee.turn_on(device)
#     await govee.set_color(device, color)
#     print(f" Light set to RGB{color}")

def main():
    print("\n Mood Check-In → Govee Light Test\n")
    scores = get_user_scores()
    print()
    normalized = compute_normalized_score(scores)
    mood = select_mood(normalized)
    print(f"\n Selected Mood: {mood}")
    
    # color = COLOR_MAP[mood] -- comment out
    # Run the async Govee call
    # asyncio.run(main(color)) -- comment out
    
    return normalized # stress score to be used in the final algorithm

if __name__ == "__main__":
    main()
