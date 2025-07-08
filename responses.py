from random import choice, randint

import re

dad_jokes = [
    "I'm afraid for the calendar. Its days are numbered.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An Impasta!",
    "How does dry skin affect you at work? You don’t have any elbow grease.",
    "What do you call cheese that isn't yours? Nacho cheese.",
    "Why couldn't the bicycle stand up by itself? It was two-tired.",
    "I'm reading a book on anti-gravity. It's impossible to put down."
]

positives = [
    "thank", "thanks", "love", "appreciate", "awesome", "great", "nice",
    "good", "happy", "joy", "joyful", "joyous", "joyfully", "joyously",
    "joyed", "joyfully", "joyously", "joyed", "joyfully", "joyously", "<3"
]
negatives = [
    "screw",
    "fuck",
    "stupid",
    "hate",
    "shit",
    "damn",
    "shit",
]

nice_responses = [
    "Aw, thanks!",
    "You're too kind! Lenny appreciates you.",
    "Right back atcha, friend!",
    "Love you too",
    "Thanks! You're awesome!",
    "We should hang out sometime!",
    "I'm glad you think so!",
]


def get_response(user_input: str) -> str:
    text = user_input.lower()
    if '!dadjoke' in text:
        return choice(dad_jokes)
    if 'crabby' in text:
        if any(p in text for p in positives):
            return choice(nice_responses)
        if any(n in text for n in negatives):
            return ":("
        return "Hello"
