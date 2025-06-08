

mock_events = [
    {
        "summary": "Team Meeting",
        "description": "Weekly sync via Zoom",
        "start": {"dateTime": "2025-06-10T10:00:00+02:00"},
        "end": {"dateTime": "2025-06-10T11:00:00+02:00"}
    }, 
    {
        "summary": "Lunch Break",
        "description": "",
        "start": {"dateTime": "2025-06-10T12:30:00+02:00"},
        "end": {"dateTime": "2025-06-10T13:00:00+02:00"}
    },
    {
        "summary": "Workout",
        "description": "Cardio session",
        "start": {"dateTime": "2025-06-10T18:00:00+02:00"},
        "end": {"dateTime": "2025-06-10T19:00:00+02:00"}
    },
    {
        "summary": "Google Meet: Project Update",
        "description": "meet.google.com/xyz",
        "start": {"dateTime": "2025-06-10T20:00:00+02:00"},
        "end": {"dateTime": "2025-06-10T21:00:00+02:00"}
    },
    {
        "summary": "Studying",
        "description": "Deep work — no meetings",
        "start": {"dateTime": "2025-06-11T09:00:00+02:00"},
        "end": {"dateTime": "2025-06-11T11:00:00+02:00"}
    },
    {
        "summary": "Call with Professor",
        "description": "Teams link inside",
        "start": {"dateTime": "2025-06-11T14:00:00+02:00c"},
        "end": {"dateTime": "2025-06-11T15:00:00+02:00"}
    },
    {
        "summary": "Creative Time",
        "description": "Time reserved for personal work",
        "start": {"dateTime": "2025-06-11T16:00:00+02:00"},
        "end": {"dateTime": "2025-06-11T18:00:00+02:00"}
    },
    {
        "summary": "Virtual Coffee Chat",
        "description": "Casual Zoom session",
        "start": {"dateTime": "2025-06-12T10:30:00+02:00"},
        "end": {"dateTime": "2025-06-12T11:00:00+02:00"}
    }
]



def classify_event(summary):

    summary = summary.lower()

    work_keywords = ["meeting", "call", "project", "sync", "update", "deadline", "review"]
    relax_keywords = ["yoga", "gym", "workout", "run", "jog", "exercise", "fitness"]
    deep_work_keywords = ["focus", "study", "studying", "thesis", "writing", "research"]
    health_keywords = ["doctor", "appointment", "dentist", "therapy", "check-up"]
    social_keywords = ["lunch", "coffee", "chat", "hangout", "break", "dinner"]
    creative_keywords = ["creative", "personal", "art", "design", "brainstorm"]

    for word in work_keywords:
        if word in summary:
            return "work"
    for word in relax_keywords:
        if word in summary:
            return "relax"
    for word in deep_work_keywords:
        if word in summary:
            return "deep work"
    for word in health_keywords:
        if word in summary:
            return "health"
    for word in social_keywords:
        if word in summary:
            return "social"
    for word in creative_keywords:
        if word in summary:
            return "creative"

    return "other"


category_to_lighting = {
    "deep work": {
        "color": "#FF0000",   # Red
        "lux": 700            # High intensity to support focus
    },
    "work": {
        "color": "#0000FF",   # Blue
        "lux": 400            # Standard office brightness
    },
    "relax": {
        "color": "#008000",   # Green
        "lux": 200            # Calming light level
    },
    "social": {
        "color": "#FFFF00",   # Yellow
        "lux": 225            # Bright, inviting
    },
    "health": {
        "color": "#FFA500",   # Orange
        "lux": 200            # Warm and energizing
    }
}


for event in mock_events:
    category = classify_event(event["summary"])
    color = category_to_lighting.get(category, "#0000FF") # If category is unknown, change light color to blue
    print(f"{event['summary']} → Category: {category}, Light Color: {color}")


