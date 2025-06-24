
import pandas as pd
from IPython.display import display
modes_data = [
    {
        "Mode": "Calm",
        "Hex": "#AEDFF7",
        "HSBK": "(200, 0.30, 0.70, 3000)",
        "Transition (ms)": 3000,
        "Use Case / Rationale": "Soft sky-blue for low-arousal relaxation.",
        "Questions": "How much are you enjoying the present moment?"
    },
    {
        "Mode": "Neutral",
        "Hex": "#FFF5B1",
        "HSBK": "(55, 0.20, 0.80, 4000)",
        "Transition (ms)": 1500,
        "Use Case / Rationale": "Gentle yellow for general tasks—uplifting without overstimulation.",
        "Questions": "How emotionally unsettled do you feel?"
    },
    {
        "Mode": "Stress Relief",
        "Hex": "#88E1A3",
        "HSBK": "(140, 0.45, 0.60, 3500)",
        "Transition (ms)": 2000,
        "Use Case / Rationale": "Restorative green to shift toward parasympathetic relaxation after stress."
    },
    {
        "Mode": "Panic",
        "Hex": "#FFA07A",
        "HSBK": "(17, 0.50, 0.50, 2700)",
        "Transition (ms)": 1000,
        "Use Case / Rationale": "Salmon-red pulsing to guide breathing and reduce acute stress."
    }
]

modes_df = pd.DataFrame(modes_data)
display(modes_df)
def calculate_lighting_mode():
    print("Please answer the following questions on a scale from 1-10:")
    
    questions = [
        ("How much are you enjoying the present moment?", "Pos"),
        ("How energized or motivated are you feeling?", "Pos"),
        (" How much is your mind racing right now? ", "Neg"),
        ("On a scale of 1 to 10, how would you rate your current mood? ", "Neg"),
        ("How calm and relaxed are you at this moment?", "pos"),
    ]
    
    scores = []
    reversed_scores = []
    
    for question, direction in questions:
        while True:
            try:
                response = int(input(question + " "))
                if 1 <= response <= 10:
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Reverse score negative items
        if direction == "Neg":
            reversed_score = response  # Higher is worse, so we don't reverse here (matches Excel)
        else:
            reversed_score = 11 - response  # Reverse positive items (higher is better)
        
        scores.append(response)
        reversed_scores.append(reversed_score)
    
    total_score = sum(reversed_scores)
    normalized_score = total_score / 50  # Normalize to 0-1 range
    
    print(f"\nTotal Score: {total_score}/50")
    print(f"Normalized Score: {normalized_score:.2f}")
    
    # Determine lighting mode based on normalized score
    if normalized_score <= 0.25:
        return "Calm"
    elif normalized_score <= 0.5:
        return "Neutral"
    elif normalized_score <= 0.75:
        return "Stress Relief"
    else:
        return "Panic"
recommended_mode = calculate_lighting_mode()
print(f"\nRecommended Lighting Mode: {recommended_mode}")

