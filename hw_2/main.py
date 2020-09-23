#!/usr/bin/env python3

import re

FILE = './stih.txt'

def filter(data):
    return re.sub('[-!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/\\n\\r\\t#]', ' ', data)

def main():
    with open(FILE) as file:
        data = file.read()

    print(filter(data))



if __name__ == '__main__':
    main()
