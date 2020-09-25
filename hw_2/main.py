#!/usr/bin/env python3

import re

FILE = './stih.txt'


# Очищает текст от знаков препинания и приводит в нижний регистр
def filter(data):
    return re.sub(' +', ' ',re.sub('[-!$…”“%^&*()_+|~=`{}\[\]:";\'<>?,.\/\\n\\r\\t#]', ' ',data)).lower()

def create_words(data):
    return [word for word in filter(data).split(' ') if len(word) != 0]


# создает N-граммы из списка слов
def create_ngram(words, n):
    ngrams = []
    lenght = len(words) - 1
    for i in range(lenght):
        if n + i > lenght:
            break
        ngrams.append(' '.join(words[i:n+i]))

    return ngrams

# создает N-граммы из текста с предваритеьной обработкой
def create_ngram_from_text(data, n): 
    words = create_words(data)
    return create_ngram(words, n)

# создает словарь частот слов/словосочетаний и т.д.
def create_freq_dict(words):
    frequency = {}
    for word in words:
        if len(word) == 0:
            continue

        if frequency.get(word) is None:
            frequency[word] = 1
        else:
            frequency[word] += 1
    return frequency

# расчет априорной вероятности слова в тексте по Линдстоуну
def prior_p_Lid(words, l = 1):
    N = len(words)
    freq = create_freq_dict(words)
    V = len(freq)
   
    prior = {}
    for word, c in freq.items():
       prior[word] = (c + l) / (N + l * V)

    return prior

# расчет условной вероятности слов в тексте по Линдстоуну
def cond_p_Lid(ngrams_dict, words_dict, l=1):
    cond = {}
    Vb = len(ngrams_dict)
    for word, word_count in words_dict.items():
        for ngram, ngram_count in ngrams_dict.items(): 
            if not ngram.startswith(word):
                continue
            first, second = ngram.split(' ')
            
            cond[(second, first)] = (ngram_count + l) / (word_count + l * Vb)
    return cond

class Text():
    def __init__(self, filename, n = 2, l = 1):
        with open(filename) as file:
            data = file.read()

        self.words = create_words(data) 
        self.N = len(self.words)
        self.Lambda = l

        self.n = n
        self.ngrams = create_ngram(self.words, n)
        
        self.words_freq = create_freq_dict(self.words)
        self.ngrams_freq = create_freq_dict(self.ngrams)
 
        self.prior_p = prior_p_Lid(self.words, self.Lambda)
        self.cond_p = cond_p_Lid(self.ngrams_freq, self.words_freq)


    def P(self, word):
        if self.prior_p.get(word) is None:
            return self.Lambda / (self.N + self.Lambda * len(self.words_freq)) 
        return self.prior_p[word]
    
    def P_cond(self, word_pair):
        if self.cond_p.get(word_pair) is not None:
            return self.cond_p[word_pair]
        else:
            second, first = word_pair
            count_first = 0
            
            if self.words_freq.get(first) is not None:
               count_first = self.words_freq[first] 

            return self.Lambda / (len(self.ngrams_freq) * self.Lambda + count_first) 
    
    def next_word(self, sentence, n):
        words = create_words(sentence) 
        if len(words) < n:
            raise RuntimeError('ngrams has not enough words')
        
        words = words[-n:]
        
        max_p = 0
        that_word = ""
         
        for word in self.words:
            res = self.P(word) 
            for ngram_word in words:
                #print('ng', ngram_word, word, self.P_cond((ngram_word, word)))
                res *= self.P_cond((ngram_word, word))
            if max_p < res:
                max_p = res
                that_word = word
        return that_word
        
    def update_n(n):
        self.ngrams = create_ngram(self.words, n)
        self.freq = create_freq_dict(self.ngrams)

def main():
    text = Text('stih.txt', 2, 1)

    sentence = 'это птица-синица'
    for i in range(10):
        sentence += ' ' + text.next_word(sentence, 3)

    print(sentence)
    

if __name__ == '__main__':
    main()
