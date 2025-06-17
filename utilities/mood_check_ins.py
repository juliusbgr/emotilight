def calculate_survey_score():
    print("Please answer the following questions on a scale from 1-10:")
    
    questions = [
        ("How much are you enjoying the present moment?", "Pos"),
        ("How energized or motivated are you feeling?", "Pos"),
        ("How much is your mind racing right now?", "Neg"),
        ("How would you rate your current mood? With 1 is most positive and 10 is most negative", "Neg"),
        ("How calm and relaxed are you at this moment?", "Pos"),
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
            reversed_score = response  # Higher is worse, so we don't reverse here
        else:
            reversed_score = 11 - response  # Reverse positive items (higher is better)
        
        scores.append(response)
        reversed_scores.append(reversed_score)
    
    total_score = sum(reversed_scores)
    normalized_score = total_score / 50  # Normalize to 0-1 range
    print(f"Total Score {total_score:.2f} Normalized Score: {normalized_score:.2f}")
    
    return normalized_score

# Run the survey on final_alogorithm.py