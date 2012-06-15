# coding=utf-8
from md5 import new as new_md5
from random import SystemRandom
from string import printable

B62_ALPHABET = printable[:62]
def convert_int2b62(num, converted=[]):
    mod = num % 62
    rem = num / 62
    converted.append(B62_ALPHABET[mod])
    if rem:
        return convert_int2b62(rem, converted)
    converted.reverse()
    retval = ''.join(converted)
    return retval

def create_token():
    randomNumberGenerator = SystemRandom()
    randomInteger = randomNumberGenerator.randint(0, 62**32)
    token = convert_int2b62(randomInteger)
    return token

if __name__ == '__main__':
    print create_token()
