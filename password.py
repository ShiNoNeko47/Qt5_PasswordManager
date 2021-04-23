import random

def generate(length, upper, numbers, special):
    chars = []
    for i in range(97, 123):
        chars.append(chr(i))
    if upper:
        for i in range(65, 91):
            chars.append(chr(i))
    if numbers:
        for i in range(48, 58):
            chars.append(chr(i))
    if special:
        for i in '!?#$%&':
            chars.append(i)
    password = ''
    for i in range(length):
        password += chars[random.randint(0, len(chars) - 1)]
    return password
