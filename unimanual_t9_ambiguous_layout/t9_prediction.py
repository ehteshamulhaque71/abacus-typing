import sys
from nltk.corpus import brown
from nltk.corpus import reuters
import nltk
from nltk.corpus import PlaintextCorpusReader
from disambiguation_trie import Trie
from next_word_prediction import GPT2

def appendwithcheck (preds, to_append):
    for pred in preds:
        if pred == to_append:
            return
    preds.append(to_append)


# def incomplete_pred(words, n):
    
#     exact, extended = t.getSuggestions(words[n-1], 1)
#     preds = []
#     if len(exact) <= 2:
#         preds = exact
#     else:
#         preds = exact[:2]
    
#     for i in range(len(extended)):
#         preds.append(extended[i])
#         if len(preds) >= 4:
#             return preds
            
#     while len(preds) < 4:
#         preds.append('')
#     return preds


def incomplete_pred(words, n):
    
    exact, extended = t.getSuggestions(words[n-1], 1)
    preds = []
    if len(exact) <= 2:
        preds = exact
    else:
        preds = exact[:4]
    
    for i in range(len(extended)):
        preds.append(extended[i])
        if len(preds) >= 4:
            return preds
            
    while len(preds) < 4:
        preds.append('')
    return preds

def preds_from_GPT(words, n):
    if n > 1:
        all_preds = gpt2.predict_next(''.join(words[:n-1]), 1000)
        # print(all_preds)
        preds = []
        for pred in all_preds:
            if pred.isalpha() and len(pred) > 1 and pred.startswith(words[n-1]):
                print(pred)
                preds.append(pred)
            if len(preds) >= 4:
                return(preds)
        while len(preds) < 4:
            preds.append('')
        return preds


def worker(string, work):
    # print(string, work)
    words=string.split()
    n=len(words)
    if work=='pred':
        all_preds = gpt2.predict_next(string, 20)
        preds = []
        for pred in all_preds:
            if pred.isalpha():
                preds.append(pred)
            if len(preds) >= 4:
                return preds
        for i in range(len(preds), 4):
            preds.append('')
        return preds
    else:
        return incomplete_pred(words, n)


new_corpus = PlaintextCorpusReader('./','.*')
tokens = new_corpus.words('../data/word-frequency-list.txt')


weighted_tokens = []
for i in range(0, len(tokens), 2):
    word = tokens[i]
    weight = int(tokens[i+1])
    if word.isalpha() and len(set(word)) >= 1:
        weighted_tokens.append([word, weight])

keys = {
    'a': 1, 'b': 1, 'c': 1,
    'd': 2, 'e': 2, 'f': 2,
    'g': 3, 'h': 3, 'i': 3,
    'j': 4, 'k': 4, 'l': 4,
    'm': 5, 'n': 5, 'o': 5,
    'p': 6, 'q': 6, 'r': 6, 's': 6,
    't': 7, 'u': 7, 'v': 7,
    'w': 9, 'x': 9, 'y': 9, 'z': 9
}

t = Trie(keys)
t.formTrie(weighted_tokens)

gpt2 = GPT2()

# print('start typing:')
# while True:
#     x = input()
#     if x[-1] == ' ':
#         print('suggestions: ', worker(x, 'pred'))
#     else:
#         print('suggestions: ', worker(x, 'med'))