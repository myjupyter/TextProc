#!/usr/bin/env python3

import re

FILE = './stih.txt'

def filter(data):
    return re.sub('[-!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/\\n\\r\\t#]', ' ', data)

def create_ngram(data, n): 
    words = re.sub(' +', ' ', filter(data)).split(' ')
    ngrams = []

    lenght = len(words) - 1
    for i in range(lenght):
        if n + i > lenght:
            break
        ngrams.append(' '.join(words[i:n+i]))

    return ngrams


def main():
    with open(FILE) as file:
        data = file.read()

    print(create_ngram(data, 1))


if __name__ == '__main__':
    main()
