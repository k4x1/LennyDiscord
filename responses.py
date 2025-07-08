from random import choice, randint

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

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '!dadjoke' or lowered == 'dad joke':
        return choice(dad_jokes)