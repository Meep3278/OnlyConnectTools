import random

ignoreChars = ".,'aeiou "

file = open('input.txt', 'r')
lines = file.readlines()
file.close()
output = ""
for line in lines:
    for ch in line.lower().strip('\n'):
        if ch in ignoreChars:
            continue
        add_ch = ch.upper()
        rand_num = random.randint(0, 4)
        if rand_num == 0:
            add_ch += " "
        output += add_ch
    output += '\n'

print(output, end = '')