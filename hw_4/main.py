#!/usr/bin/env python3

import math as m

COND_PROB = {
    '<s>' : {'<s>': 0.0, 'ADJ': 0.2,  'N': 0.2,  'V': 0.1,  'CONJ': 0.01, 'DET': 0.4},
    'ADJ' : {'<s>': 0.0, 'ADJ': 0.2,  'N': 0.2,  'V': 0.05, 'CONJ': 0.2,  'DET': 0.01},
    'N'   : {'<s>': 0.0, 'ADJ': 0.05, 'N': 0.01, 'V': 0.5,  'CONJ': 0.2,  'DET': 0.01},
    'V'   : {'<s>': 0.0, 'ADJ': 0.1,  'N': 0.2,  'V': 0.01, 'CONJ': 0.2,  'DET': 0.3},
    'CONJ': {'<s>': 0.0, 'ADJ': 0.1,  'N': 0.2,  'V': 0.2,  'CONJ': 0.0,  'DET': 0.2},
    'DET' : {'<s>': 0.0, 'ADJ': 0.3,  'N': 0.7,  'V': 0.0,  'CONJ': 0.0,  'DET': 0.0}, 
}

PROBS = {
    'time' : {'N': 0.01,   'V': 0.001, 'ADJ': 0.0005, '<s>': 0.0, 'DET': 0.0, 'CONJ': 0.0},
    'flies': {'N': 0.0005, 'V': 0.01,  'ADJ': 0.0,  '<s>': 0.0, 'DET': 0.0, 'CONJ': 0.0},
    'like' : {'N': 0.001,  'V': 0.02,  'ADJ': 0.0,  '<s>': 0.0, 'DET': 0.0, 'CONJ': 0.05},
    'an'   : {'N': 0.0,    'V': 0.0,   'ADJ': 0.0,  '<s>': 0.0, 'DET': 0.01,'CONJ': 0.0},
    'arrow': {'N': 0.01,   'V': 0.0,   'ADJ': 0.01, '<s>': 0.0, 'DET': 0.0, 'CONJ': 0.0},
}

SENT = 'Time flies like an arrow'

def prior_vector(word, past_part):
    return {part: PROBS[word][part] * conf_prob for part, conf_prob in COND_PROB[past_part].items()}

def stage(word, past_part, past_stage):
    return {part : max([prob * COND_PROB[past_part][part] for part, prob in past_stage.items()]) * conf_prob for part, conf_prob in COND_PROB[past_part].items()}

def text_proc(text):
    splitted_text = ['<s>']
    splitted_text.extend(text.lower().split())
    return splitted_text

def main():
    print(text_proc(SENT))    
    p = prior_vector('time', '<s>')
    print(stage('flies', max(p.items(), key=lambda x: x[1])[0], p)) 

if __name__ == '__main__':
    main()
