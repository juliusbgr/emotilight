# mood_light_sim.py
questions = [
    "How much is your mind racing right now? (1–10): ",
    "How anxious or stressed are you feeling right now? (1–10): ",
    "How emotionally unsettled do you feel? (1–10): ",
    "How out of control do your emotions feel right now? (1–10): "
]

PRESETS = {
    "Deep Rest":      {"hue": 190, "sat": 0.30, "bri": 0.40, "kelvin": 3100},
    "Calm":           {"hue": 200, "sat": 0.30, "bri": 0.70, "kelvin": 3000},
    "Stress Relief":  {"hue": 140, "sat": 0.45, "bri": 0.60, "kelvin": 3500},
    "Panic":          {"hue": 17,  "sat": 0.50, "bri": 0.50, "kelvin": 2700}
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
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Enter an integer.")
    return scores

def compute_normalized_score(scores):
    total = sum(scores)
    normalized = total / (len(scores) * 10)
    return total, normalized

def select_mood(normalized):
    if normalized <= 0.25:
        return "Deep Rest"
    elif normalized <= 0.50:
        return "Calm"
    elif normalized <= 0.75:
        return "Stress Relief"
    else:
        return "Panic"

def simulate_light(mood):
    cfg = PRESETS[mood]
    print("\nSuggested Light Mode:")
    print(f"Mode: {mood}")
    print(f"HSBK: H={cfg['hue']}°, S={cfg['sat']}, B={cfg['bri']}, K={cfg['kelvin']}")

def main():
    print("\nMood Check-In (4 questions, scale 1–10)\n")
    scores = get_user_scores()
    total, normalized = compute_normalized_score(scores)
    mood = select_mood(normalized)
    
    print(f"\nTotal score: {total} / 40")
    print(f"Normalized score: {normalized:.2f}")
    simulate_light(mood)

if __name__ == "__main__":
    main()
