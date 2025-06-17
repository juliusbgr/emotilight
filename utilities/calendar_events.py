from dateutil import parser
import pandas as pd

mock_events = [
    {
        "summary": "Team Meeting",
        "description": "Weekly sync via Zoom",
        "start": {"dateTime": "2025-06-17T10:00:00+02:00"},
        "end": {"dateTime": "2025-06-17T11:00:00+02:00"}
    }, 
    {
        "summary": "Lunch Break",
        "description": "",
        "start": {"dateTime": "2025-06-17T12:30:00+02:00"},
        "end": {"dateTime": "2025-06-17T13:00:00+02:00"}
    },
    {
        "summary": "Workout",
        "description": "Cardio session",
        "start": {"dateTime": "2025-06-17T18:00:00+02:00"},
        "end": {"dateTime": "2025-06-17T19:00:00+02:00"}
    },
    {
        "summary": "Google Meet: Project Update",
        "description": "meet.google.com/xyz",
        "start": {"dateTime": "2025-06-17T20:00:00+02:00"},
        "end": {"dateTime": "2025-06-17T21:00:00+02:00"}
    },
    {
        "summary": "Studying",
        "description": "Deep work — no meetings",
        "start": {"dateTime": "2025-06-18T09:00:00+02:00"},
        "end": {"dateTime": "2025-06-18T11:00:00+02:00"}
    },
    {
        "summary": "Call with Professor",
        "description": "Teams link inside",
        "start": {"dateTime": "2025-06-18T13:00:00+02:00"},
        "end": {"dateTime": "2025-06-18T14:30:00+02:00"}
    },
    {
        "summary": "Creative Time",
        "description": "Time reserved for personal work",
        "start": {"dateTime": "2025-06-18T16:00:00+02:00"},
        "end": {"dateTime": "2025-06-18T18:00:00+02:00"}
    },
    {
        "summary": "Virtual Coffee Chat",
        "description": "Casual Zoom session",
        "start": {"dateTime": "2025-06-19T10:30:00+02:00"},
        "end": {"dateTime": "2025-06-19T11:00:00+02:00"}
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


# Stress levels mapping
stress_mapping = {
    "work": 0.85,
    "deep work": 0.60,
    "health": 0.75,
    "relax": 0.15,
    "social": 0.2,
    "creative": 0.35,
    "other": 0.5
}


event_data = []

for event in mock_events:
    summary = event["summary"]
    start = parser.isoparse(event["start"]["dateTime"])
    end = parser.isoparse(event["end"]["dateTime"])
    event_type = classify_event(summary)
    stress = stress_mapping.get(event_type, 0.5)
    event_data.append({
        "summary": summary,
        "start": start,
        "end": end,
        "event_type": event_type,
        "stress_level": stress
    })

df = pd.DataFrame(event_data)
print(df)