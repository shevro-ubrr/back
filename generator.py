from string import ascii_letters, digits
from random import choice

def generate_username(length=8):
    return ''.join(choice(ascii_letters + digits) for _ in range(length))