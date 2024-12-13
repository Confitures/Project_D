from django import template
from fuzzywuzzy import process
# import logging

register = template.Library()


def replace_character(word: str) -> str:
    s = {'!', '@', '#', '$', '%', '^', '&', '(', ')', '{', '}', '[', ']', '?', '<', '>', ',', '.', ' '}
    return ''.join(['*' if c not in s else c for c in word])


@register.filter()  #
def censor(text) -> str:
    text = text.split()
    s_c = 91
    l = {'obscenus', 'непристойный', 'распутный', 'безнравственный', 'luck'}  # перечень нецензурных слов
    for i, word in enumerate(text):
        if process.extractOne(word, l, score_cutoff=s_c):
            text[i] = replace_character(word)
    return ' '.join(text)
