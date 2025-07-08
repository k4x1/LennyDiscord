from random import choice


#this stuff is all hard coded for now
cosmetics = {
    "HardHat": "A sturdy hard hat",
    "WizzardHat": "A magical wizard hat",
    "PropellorHat": "A hat with a propeller",
    "TricornHat": "A three-cornered hat",
    "DetectiveHat": "A detective's hat",
    "Cigarette": "A cigarette accessory"
}

def get_cosmetic_keys_help() -> str:
    return "\n".join(f"`{k}`: {v}" for k, v in cosmetics.items())

def is_valid_cosmetic_key(key: str) -> bool:
    return key in cosmetics

#everything below here is just silly stuff

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

# vscode copilot is kinda amazing at just geneerating these
positives = [
    "thank", "thanks", "love", "appreciate", "awesome", "great", "nice",
    "good", "happy", "<3", "heart", "kind", "cool", "best", "amazing", "fantastic", "wonderful",
    "excellent", "brilliant", "super", "fantabulous", "rad", "radical", "dope", "lit", "sick", "sweet", "neat", "fabulous", "magnificent", "terrific"  
]
negatives = [
    "screw",
    "fuck",
    "stupid",
    "hate",
    "shit",
    "damn",
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

