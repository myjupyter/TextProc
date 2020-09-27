#!/usr/bin/env python3

import re
import math

FILE = './stih.txt'


# Очищает текст от знаков препинания и приводит в нижний регистр
def filter(data):
    return re.sub(' +', ' ',re.sub('[-!$…”“%^&*()_+|~=`{}\[\]:";\'<>?,.\/\\n\\r\\t#]', ' ',data)).lower()

def create_words(data):
    return [word for word in filter(data).split(' ') if len(word) != 0]

# создает N-граммы из списка слов
def create_ngram(words, n = 2):
    ngrams = []
    lenght = len(words)
    for i in range(lenght):
        if n + i > lenght:
            break
        ngrams.append(' '.join(words[i:n+i]))

    return ngrams

# создает словарь частот слов/словосочетаний и т.д.
def create_freq_dict(words):
    frequency = {}
    for word in words:
        if frequency.get(word) is None:
            frequency[word] = 1
        else:
            frequency[word] += 1
    return frequency

class Dictionary():
    def __init__(self, text, n = 2):
        self.n = n
        self.words = create_words(text)
        
        self.ngrams_list = [self.words]
        self.ngrams_freq_dict_list = [create_freq_dict(self.words)]
        for i in range(1, n + 1):
            self.ngrams_list.append(create_ngram(self.words, i + 1))
            self.ngrams_freq_dict_list.append(create_freq_dict(self.ngrams_list[-1]))

    def P_Lid(self, sentence, l = 0):
        splitted_sentence = create_words(sentence)
        word_count = len(splitted_sentence)
        if word_count > self.n + 1:
            raise AttributeError('Dictionary has only {:d}-grams'.format(self.n))
        
        processed_sentence = ' '.join(splitted_sentence)

        if (freq := self.ngrams_freq_dict_list[word_count - 1].get(processed_sentence)) is not None:
            return (freq + l) / (len(self.words) + l * len(self.ngrams_freq_dict_list[word_count - 1]))
        return l / (len(self.words) + l * len(self.ngrams_freq_dict_list[word_count - 1]))

    def P_Lid_Cond(self, word, sentence, l = 0):
        splitted_sentence = create_words(sentence)
        splitted_word     = create_words(word)
        word_count = len(splitted_sentence)
        if word_count > self.n:
            raise AttributeError('Dictionary has only {:d}-grams'.format(word_count))
       
        N = len(self.words)
        C_n = self.P_Lid(' '.join(splitted_sentence + splitted_word), 0) * N 
        C_n_1 = self.P_Lid(' '.join(splitted_sentence), 0) * N
        
        return (C_n + l) / (C_n_1 + l * len(self.ngrams_freq_dict_list[word_count - 1]))
    

class Text():
    def __init__(self, filename, n = 2):
        with open(filename) as file:
            raw_text = file.read()
        
        self.n = n
        self.dictionary = Dictionary(raw_text, n)

    def next_word_by_Lid_smoothing(self, sentence, l = 0): 
        max_probability = -(1 << 60)
        max_probability_word = ""
        processed_sentence = ' '.join(create_words(sentence)[-self.n:])
        for word in self.dictionary.words:
            if (p := self.dictionary.P_Lid_Cond(word, processed_sentence, l)) > max_probability:
                max_probability = p
                max_probability_word = word

        return max_probability_word

             
    def next_word_by_WB_smoothing(self, sentence):
        pass

def main():
    text = Text('big.txt', 3)

    sentence = 'А еще были'
    for i in range(40):
        sentence += ' ' + text.next_word_by_Lid_smoothing(sentence, 1)

    print(sentence)

if __name__ == '__main__':
    main()
