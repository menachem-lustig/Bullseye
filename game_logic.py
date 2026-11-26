import random
from data import colors

def generate_secret_code():
    selected_colors = []
    for i in range(4):
        while True:
            color = random.choice(colors)
            if color not in selected_colors:
                selected_colors.append(color)
                break   
    return selected_colors

def validate_guess(guessed_colors):
    valid = []
    if len(guessed_colors) != 4:
        return None
    for color in guessed_colors:
        color.lower()
        if color in valid or color not in colors:
            return None
        valid.append(color)
    return valid

def score_guess(guessed_colors, secret_code):
    bools= 0
    hits = 0
    for index,color in enumerate(guessed_colors):
        if color in secret_code:
            if guessed_colors[index] == secret_code[index]:
                hits +=1
            else:
                bools +=1
    return bools,hits



