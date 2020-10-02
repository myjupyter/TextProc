#!/usr/bin/env python3

import re
import math

# Очищает текст от знаков препинания и приводит в нижний регистр
def filter(data):
    return re.sub(' +', ' ',re.sub('[-!$…”“%^&*()_+|~=`{}\[\]:";\'<>?,.\/\\n\\r\\t#]', ' ',data)).lower()

# По тексту создает отфильтрованные слова, приведенные в нижний регистр
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

    @property
    def dictionary(self):
        return self.ngrams_freq_dict_list[0]

    def P_Lid(self, sentence, l = 0):
        splitted_sentence = create_words(sentence)
        word_count = len(splitted_sentence)
        if word_count > self.n + 1:
            raise AttributeError('Dictionary has only {:d}-grams'.format(self.n))
        
        processed_sentence = ' '.join(splitted_sentence)

        if (freq := self.ngrams_freq_dict_list[word_count - 1].get(processed_sentence)) is not None:
            return (freq + l) / (len(self.words) + l * len(self.ngrams_freq_dict_list[word_count - 1]))
        return l / (len(self.words) + l * len(self.ngrams_freq_dict_list[word_count - 1]))
    
    def perplexity(self, sentence, n = 1, l = 0):
        if n > self.n + 1:
            raise AttributeError('Dictionary has only {:d}-grams'.format(self.n)) 

        splitted_sentence = create_words(sentence)
        word_count = len(create_words(sentence)) 

        p = 1
        if n == 1:
            p = math.prod([self.P_Lid(word, l) for word in splitted_sentence])    
        else:
            for i in range(n - 1, len(splitted_sentence)):
                p *= self.P_Lid_Cond(splitted_sentence[i], ' '.join(splitted_sentence[i-n+1:i]),l)
                     
        return  (1 / p) ** (1 / word_count) if p > 0 else float('inf') 


    def P_Lid_Cond(self, word, sentence, l = 0):
        splitted_sentence = create_words(sentence)
        splitted_word     = create_words(word)
        word_count = len(splitted_sentence)
        if word_count > self.n:
            raise AttributeError('Dictionary has only {:d}-grams'.format(self.n))
       
        N = len(self.words)
        C_n = self.P_Lid(' '.join(splitted_sentence + splitted_word), 0) * N 
        C_n_1 = self.P_Lid(' '.join(splitted_sentence), 0) * N
        if l == 0 and C_n == 0 and C_n_1 == 0:
            return 0

        return (C_n + l) / (C_n_1 + l * len(self.ngrams_freq_dict_list[word_count - 1]))
    
    def __lambda(self, sentence):
        splitted_sentence = create_words(sentence)
        word_count = len(splitted_sentence)
        if word_count > self.n:
            raise AttributeError('Dictionary has only {:d}-grams'.format(self.n))
       
        processed_sentence = ' '.join(splitted_sentence)
        C = self.ngrams_freq_dict_list[word_count - 1].get(processed_sentence)

        if C is None:
            return 0

        N_1 = sum(map(lambda x: 1 if x[0].startswith(processed_sentence) else 0, self.ngrams_freq_dict_list[word_count].items()))
        return C / (N_1 + C)

    def P_WB_Cond(self, word, sentence):   
        if len(sentence) > 0:
            L = self.__lambda(sentence)
            splitted_sentence = create_words(sentence)
            new_sentence = ' '.join(splitted_sentence[-len(splitted_sentence) + 1:]) if len(splitted_sentence) > 1 else '' 
            return L * self.P_Lid_Cond(word, sentence) + (1 - L) * self.P_WB_Cond(word, new_sentence)
        else:
            return  self.P_Lid(word, 1)


class Text():
    def __init__(self, filename, n = 2):
        with open(filename) as file:
            raw_text = file.read()
        
        self.n = n
        self.dictionary = Dictionary(raw_text, n)

    def next_word(self, sentence, method):
        max_probability = -(1 << 60)
        max_probability_word = ''
        processed_sentence = ' '.join(create_words(sentence)[-self.n:])
       
        p_cond = 0
        if method[0] == 'Lid':
            p_cond = self.dictionary.P_Lid_Cond
            method = (method[1],)
        elif method[0] == 'WB':
            p_cond = self.dictionary.P_WB_Cond
            method = ()
        else:
            raise AttributeError('Wrong mehtod')
        
        for word in self.dictionary.dictionary.keys():
            if (p := p_cond(word, processed_sentence, *method)) > max_probability:
                max_probability = p
                max_probability_word = word

        return max_probability_word
    
    @property 
    def words(self):
        return self.dictionary.dictionary
    
    def make_stat_to_csv(self, ngram_size, other_text): 
        for n in range(1, ngram_size + 1): 
            with open(str(n) + '-gramm.csv', 'w') as file:
                file.write(str(n) + '-gramm;P(w|w1...wn)\n')
                for ngram in other_text.dictionary.ngrams_freq_dict_list[n-1].keys(): 
                    if n == 0:
                        file.write('{:s};{:3f}\n'.format(ngram, self.dictionary.P_Lid(ngram, 1)))
                    else:
                        words = create_words(ngram)
                        file.write('{:s};{:3f}\n'.format(ngram, self.dictionary.P_WB_Cond(words[0], ' '.join(words[:-1]))))        

def main():
    learn = Text('learn.txt', 5)
    test = Text('test.txt', 5)

    # Запись статистики
    learn.make_stat_to_csv( 5, test)

    # Пример генерации текста
    text = Text('stih.txt', 2)
    sentence = 'А это'
    for i in range(20):
        sentence += ' ' + text.next_word(sentence, ('WB',))    
    print(sentence)

if __name__ == '__main__':
    main()
