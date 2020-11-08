#!/usr/bin/env python3

import pymorphy2 
import re
import math
from collections import Counter

morph = pymorphy2.MorphAnalyzer()

# Очищает текст от знаков препинания и приводит в нижний регистр
def filter(data):
    return re.sub(' +', ' ',re.sub('[-!$…”“%^&*()_+|~=`{}\[\]:";\'<>?,.\/\\n\\r\\t#]', ' ',data)).lower()

# По тексту создает отфильтрованные слова, приведенные в нижний регистр
def create_words(data):
    return [word for word in filter(data).split(' ') if len(word) != 0]

class Text:
    def __init__(self, filename):
        with open(filename) as file:
           self.__words = [morph.parse(word)[0] for word in create_words(file.read())]

    def bigram(self):
        bigram_list = list() 
        adjs = ('ADJF', 'ADJS')
        w = self.__words
        for i in range(1, len(self.__words)):
            if 'NOUN' in w[i].tag.grammemes and any(list(map(lambda x: x in w[i-1].tag.grammemes, adjs))): 
                bigram_list.append((self.__words[i-1].normal_form, self.__words[i].normal_form)) 
        return Counter(bigram_list) 
    
    def unigram(self):
        return Counter([w.normal_form for w in self.__words])

    @property
    def words(self):
        return self.__words


def return_MIlist(d, bd):
    N = len(d)
    return {b : math.log((bcount**3) * N / (d[b[0]] * d[b[1]])) for b, bcount in bd.items()}
        

def main():
    text = Text('book.txt')
   # l = sorted(text.bigram().items(), key=lambda x: x[1], reverse=True)
   # with open('freq.res', 'w') as file:
   #     file.writelines(list(map(lambda x: ' '.join(list(x[0]))+' '+str(x[1])+'\n' , l))[:20])

    d = text.unigram()
    bd = text.bigram()
    s = sorted(return_MIlist(d, bd).items(), key=lambda x: x[1], reverse=True) 

    with open('MI.res', 'w') as file:
        file.writelines(list(map(lambda x: ' '.join(list(x[0]))+' '+str(x[1])+'\n' , s))[:20])

if __name__ == '__main__':
    main()
