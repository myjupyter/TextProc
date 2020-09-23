#!/usr/bin/env python3
import re
import argparse

LINE_PATTERN = '{:s};{:d}\n'

def init_parser():
    parser = argparse.ArgumentParser(description='Words frequency')
    parser.add_argument('-i', '--input', help='file name of incoming text', type=str, required=True)
    parser.add_argument('-o', '--output', help='result .csv text', default='result.csv', type=str)
    parser.add_argument('-a', '--accuracy', help='accuracy of frequency', type=int, default=6)
    return parser.parse_args()

def getwordslist(data):
    return (re.sub('[-!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/\\n\\r\\t#]', ' ', data)).split(' ')

def writestat(data_dict, out, acc):
    words_count = sum(data_dict.values())
    with open(out, 'w') as file:
        worddict = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
        file.writelines([
            LINE_PATTERN.format(key, value ) for key, value in worddict
        ])

def main():
    args = init_parser()

    with open(args.input) as file:
        read_data = file.read()
  
    words = dict()
    for word in getwordslist(read_data):
        lword = word.lower()
        if lword in words:
            words[lword] += 1
        else:
            words[lword] = 1 

    if '' in words:
        del words['']

    writestat(words, args.output, args.accuracy)
   

if __name__ == '__main__':
    main()
