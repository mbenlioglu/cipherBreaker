"""
    Created by mbenlioglu on 10/4/2017
"""
import csv
from src.strings import paths


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


def monogram_frequency_analysis(cipher_text, lang='en_us'):
    """
    Analyzes the cipher text for monogram frequencies of letters for ciphers that preserve language statistics while
    encrypting the plain text
    :param cipher_text: Encrypted text to be analyzed.
    :type cipher_text: str
    :param lang: Language in which analysis will take place. Default is 'en-us'
    :type lang: str
    :return: A dictionary that contains the list of cipher text's monogram frequencies and recommended encryption shift
    to match this cipher text
    """
    letter_freq = [0] * 26

    cipher_text = cipher_text.upper()

    # count frequencies in cipher text
    for c in cipher_text:
        if c.isupper():
            letter_freq[ord(c) - 65] += 1

    cipher_frequencies = []
    for i, count in enumerate(letter_freq):
        cipher_frequencies.append((str(chr(i + 97)), count))
    del letter_freq[:]
    cipher_frequencies = sorted(cipher_frequencies, key=lambda x: x[1], reverse=True)

    # load real frequency values for language
    real_frequencies = []
    with open(getattr(paths, lang + '_monogram_freq')) as f:
        csvr = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in csvr:
            real_frequencies.append((row['letter'], row['freq']))
    real_frequencies = sorted(real_frequencies, key=lambda x: x[1], reverse=True)
    real_freq_order = {real_frequencies[x][0]: x for x in range(len(real_frequencies))}

    # calculate mean error for all substitutions, recommendation is the one that gives the closest error to 0
    lowest_error = float('inf')
    lowest_error_shift = 0
    for substitution in real_frequencies:
        # shift amount required to assign most frequent letter in cipher to our current replacement for it
        decryption_shift = get_letter_num(substitution[0]) - get_letter_num(cipher_frequencies[0][0])
        encryption_shift = -decryption_shift % 26
        cur_error = 0
        for i, l in enumerate(cipher_frequencies):
            cur_error += abs(i - real_freq_order[chr(shift(ord('a'), ord('z'), ord(l[0]), decryption_shift))])
        cur_error = float(cur_error) / 26
        if cur_error < lowest_error:
            lowest_error = cur_error
            lowest_error_shift = encryption_shift

    return {'recommended': lowest_error_shift, 'frequencies': cipher_frequencies}


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


def get_letter_num(letter):
    """
    :type letter: chr
    :return:
    """
    if letter.isupper():
        return ord(letter) - 65
    elif letter.islower():
        return ord(letter) - 97
    else:
        raise ValueError
