#!/usr/bin/env python3

import numpy
import matplotlib.pyplot as plt


def main():
    with open('result.csv') as file:
        data = file.read().split('\n')
    
    freq = [int(s.split(';')[1]) for s in data if len(s) != 0]
    
    freq = [f for f in freq if f > 100]

    plt.plot([i for i in range(len(freq))], freq)
    plt.savefig('res.png')

if __name__ == '__main__':
    main()

