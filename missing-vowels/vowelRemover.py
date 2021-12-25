#include <stdio.h>
import random
import sys

# input = sys.argv[1]
file = open('input.txt', 'r')
lines = file.readlines()
for input in lines:
    output = ""
    for ch in input:
        if(ch=='.' or ch==',' or ch=='\'' or ch=='A' or ch=='a' or ch=='E' or ch =='e' or ch=='I' or ch=='i' or ch=='O' or ch=='o' or ch=='U' or ch=='u' or ch==' '):
            continue
        add_ch = ch.capitalize()
        rand_num = random.randint(0, 4)
        if rand_num == 0:
            add_ch += " "
        output += add_ch
    print(output)
