#!/usr/bin/python3
import random
import sys
import time

if __name__ == '__main__':
    correct = 0
    questions = 0
    start = int(time.time())

    while True:
        fakt1 = random.randint(1, 10)
        fakt2 = random.randint(1, 10)
        product = input('Vad är {} * {}? '.format(fakt1, fakt2))

        if product == '':
            end = int(time.time())
            print('Du hade {} rätt av {} frågor.'.format(correct, questions))
            print('Du höll på i {} sekunder'.format(end-start))
            sys.exit()

        questions += 1
        if int(product) == (fakt1 * fakt2):
            print('Rätt!! 1 poäng')
            correct += 1
        else:
            print('Tyvärr, rätt svar är {}'.format((fakt1*fakt2)))
