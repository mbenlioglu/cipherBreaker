"""
    Created by mbenlioglu on 10/4/2017
"""
import csv
from ..strings import paths


def shift(low, high, val, amount):
    """
    Shifts the given number (:param val) with given shift amount (:param shift) in a circular manner, where :param low
    and :param high are the limits (modulo like)
    :type low: int
    :type high: int
    :type val: int
    :type amount: int
    :return: shifted number
    """
    base = high - low + 1
    if amount < 0:
        amount += base
    return low + (val + amount - low) % base


def monogram_frequency_analysis(cipher_text, lang='en-us'):
    """
    Analyzes the cipher text for monogram frequencies of letters for ciphers that preserve language statistics while
    encrypting the plain text
    :param cipher_text: Encrypted text to be analyzed.
    :type cipher_text: str
    :param lang: Language in which analysis will take place. Default is 'en-us'
    :type lang: str
    :return: A dictionary that contains the list of cipher text's monogram frequencies and recommended shift amount to
    match this cipher text
    """
    letter_freq = [0] * 26

    cipher_text = cipher_text.upper()

    # count frequencies in cipher text
    for c in cipher_text:
        if c.isupper():
            letter_freq[ord(c) - 65] += 1

    # load real frequency values for language
    real_frequencies = {}
    with open(getattr(paths, lang + '_monogram_freq')) as f:
        csvr = csv.DictReader(f, delimiter=',', quotochar='"')
        for row in csvr:
            real_frequencies[row['letter']] = row['freq']

    # todo: finish here


def multiplicative_inverse(num, modulo):
    t = 0
    r = modulo
    newt = 1
    newr = num

    while newr != 0:
        quotient = r / newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise ValueError('number does not have a multiplicative inverse in given modulo')
    return t if t > 0 else t + modulo
