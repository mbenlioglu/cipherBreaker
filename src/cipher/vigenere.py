"""
    Created by mbenlioglu on 10/3/2017
"""
import collections
import string
from _cipher_utils import shift
from src.strings import paths
import caesar


# ======================================================================================================================
# Public
# ======================================================================================================================
def encrypt(text, passkey):
    """
    Encryption with given passkey using vigenere cipher
    :param text: Plain text to be encrypted
    :type text: str
    :param passkey: Passkey to be used in encryption. Should only contain [A-Za-z]
    :type passkey: str
    :return: Encrypted cipher text
    """
    int_passkey = [ord(c.upper()) - 65 for c in passkey]

    cipher_text = list(text)
    i = 0
    pass_i = 0
    while i < len(text):
        if text[i].isupper():
            cipher_text[i] = chr(shift(ord('A'), ord('Z'), ord(text[i]), int_passkey[pass_i % len(int_passkey)]))
            i += 1
            pass_i += 1
        elif text[i].islower():
            cipher_text[i] = chr(shift(ord('a'), ord('z'), ord(text[i]), int_passkey[pass_i % len(int_passkey)]))
            i += 1
            pass_i += 1
        else:
            i += 1

    return ''.join(cipher_text)


def decrypt(cipher_text, passkey):
    """
    Reverse encryption operation using Vigenere cipher
    :param cipher_text: Encrypted text to decrypt
    :type cipher_text: str
    :param passkey: Passkey used to encrypt this text. Should only contain [A-Za-z]
    :type passkey: str
    :return: Decryption result
    """
    reverse_passkey = []
    for c in passkey:
        neg = (-ord(c)) % 26
        while neg < 65:
            neg += 26
        reverse_passkey.append(chr(neg))
    # reverse_passkey = [chr(52 + (-ord(c)) % 26) for c in passkey]
    return encrypt(cipher_text, ''.join(reverse_passkey))


def force_break(cipher_text, lang='en_us'):
    """
    Applies frequency analysis of overlapping letters with cipher text and rotated versions of it to guess passkey
    length, from there cipher text is broken into smaller shift ciphers and plain text is guessed through applying
    monogram frequency analysis.
    :param cipher_text: Encrypted text using Vinegere cipher
    :type cipher_text: str
    :param lang: Language of original text default is 'en-us'
    :type lang: str
    :return: Extracted passkey and plain text from the encrypted text
    """
    # load lookup table of words for language
    dict_name = lang + '_words'
    f = open(getattr(paths, dict_name), 'r')
    word_set = frozenset(x.upper() for x in f.read().splitlines())
    f.close()

    # cipher text stripped from spaces and punctuation
    cipher_only_letter = cipher_text.translate(None, string.punctuation + ' ')

    # Start with small estimated key length, increase the predetermined max key length and repeat until we find a
    # sufficient decryption result.
    min_key = 0
    j = 2
    while j < len(cipher_text):
        key_length = _passkey_length_guess(cipher_text, min_key, j)
        sub_ciphers = [cipher_only_letter[i::key_length] for i in range(key_length)]

        passkey = []
        for sub in sub_ciphers:
            caesar_result = caesar.force_break(''.join(sub), lang, 'freq')
            passkey.append(chr(caesar_result[0]['shift'] + 65))

        match_count = 0
        decrypted = decrypt(cipher_text, ''.join(passkey))
        # check matching percentage of words in decrypted text
        for word in decrypted.split():
            word = str(word).translate(None, string.punctuation + ' ')
            if word.upper() in word_set:
                match_count += 1

        # accept result if match rate is over 90%
        if float(match_count) / len(cipher_text.split()) >= 0.9:
            return {'passkey': ''.join(passkey), 'decrypted': decrypted}
        else:
            min_key = j
            j *= 2
    raise Exception('No result found!')


# ======================================================================================================================
# Private
# ======================================================================================================================
def _passkey_length_guess(cipher_text, min_shift, max_shift):
    """
    Rotates the cipher text 1 letter at a time and counts the number of overlapping characters. Returns the smallest
    rotation count that gives the most coincidences
    :param cipher_text: Encrypted text
    :type cipher_text: str
    :param min_shift: Predetermined min shift amount (i.e. don't return smaller than this number)
    :type min_shift: int
    :param max_shift: Predetermined max shift amount (i.e. don't return bigger than this number)
    :type max_shift: int
    :return: Estimated key length
    """
    max_overlap = -1
    max_shift_count = -1

    cipher_only_letter = cipher_text.translate(None, string.punctuation + ' ')
    ct_deque = collections.deque(cipher_only_letter)

    if max_shift > len(cipher_only_letter) - 1:
        max_shift = len(cipher_only_letter) - 1

    if min_shift > 0:
        ct_deque.rotate(min_shift)

    for s in range(min_shift, max_shift):
        ct_deque.rotate(1)
        cur_overlap = 0
        for i, c in enumerate(cipher_only_letter):
            if c == ct_deque[i]:
                cur_overlap += 1
        if cur_overlap > max_overlap:
            max_overlap = cur_overlap
            max_shift_count = s + 1

    return max_shift_count
