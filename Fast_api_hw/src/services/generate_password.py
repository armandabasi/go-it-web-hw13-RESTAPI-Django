import random
import string


def generate_password():
    letter = random.choice(string.ascii_letters)
    digit = random.choice(string.digits)
    symbols = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    password = letter + digit + symbols
    password = ''.join(random.sample(password, len(password)))
    return password


password = generate_password()
print(password)
