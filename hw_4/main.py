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

def new_stage(word, past_part, past_stage):
    return {part : max([past_stage[p] * COND_PROB[past_part][part] for p in past_stage.keys()]) * prob for part, prob in PROBS[word].items()}

def text_proc(text):
    return text.lower().split()

def Viterbi(text):
    text = text_proc(text)
    stage = prior_vector(text[0], '<s>')
    
    hidden_state = [max(stage.items(), key=lambda x: x[1])[0]]
    del text[0]
    for word in text:
        stage = new_stage(word, hidden_state[-1], stage)
        hidden_state.append(max(stage.items(), key=lambda x: x[1])[0])

    return hidden_state

def main():
    hs = Viterbi(SENT)
    print(hs)

if __name__ == '__main__':
    main()
