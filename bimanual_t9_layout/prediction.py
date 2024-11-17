import sys
from nltk.corpus import brown
from nltk.corpus import reuters
import nltk
from nltk.corpus import PlaintextCorpusReader
from weighted_trie import Trie
from next_word_prediction import GPT2

def appendwithcheck (preds, to_append):
    for pred in preds:
        if pred == to_append:
            return
    preds.append(to_append)


def incomplete_pred(words, n):
    
    preds = t.getAutoSuggestions(words[n-1])
    # if n == 1:
    #     return preds
    # gpt_preds = preds_from_GPT(words, n)
    # if len(preds) > 2:
    #     preds = preds[:2]
    # for pred in gpt_preds:
    #     preds.append(pred)
    #     if len(preds) >= 4:
    #         return preds
    # while (len(preds) < 4):
    #     preds.append('')
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
    if word.isalpha() and len(word) > 1 and len(set(word)) > 1:
        weighted_tokens.append([word, weight])

t = Trie()
t.formTrie(weighted_tokens)
gpt2 = GPT2()

# print('start typing:')
# while True:
#     x = input()
#     if x[-1] == ' ':
#         print('suggestions: ', worker(x, 'pred'))
#     else:
#         print('suggestions: ', worker(x, 'med'))