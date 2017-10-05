"""
    Created by mbenlioglu on 10/3/2017
"""
import collections
from _cipher_utils import shift
import ceasar


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
    for i, c in enumerate(text):
        if c.isupper():
            cipher_text[i] = chr(shift(ord('A'), ord('Z'), ord(c), int_passkey[i % len(int_passkey)]))
        elif c.islower():
            cipher_text[i] = chr(shift(ord('a'), ord('z'), ord(c), int_passkey[i % len(int_passkey)]))

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
    reverse_passkey = [chr(91 - ord(c.upper())) for c in passkey]
    return encrypt(cipher_text, ''.join(reverse_passkey))


def force_break(cipher_text):
    """
    Applies frequency analysis of overlapping letters with cipher text and rotated versions of it to guess passkey
    length, from there cipher text is broken into smaller shift ciphers and plain text is guessed through applying
    monogram frequency analysis.
    :param cipher_text: Encrypted text using Vinegere cipher
    :type cipher_text: str
    :return: Extracted plain text from the encrypted text
    """
    key_length = _passkey_length_guess(cipher_text)
    sub_ciphers = [cipher_text[i::key_length] for i in range(key_length)]

    resolved = [ceasar.force_break(''.join(sub), method='freq') for sub in sub_ciphers]

    return ''.join([c for l in zip(*resolved) for c in l])


# ======================================================================================================================
# Private
# ======================================================================================================================
def _passkey_length_guess(cipher_text):
    """
    Rotates the cipher text 1 letter at a time and counts the number of overlapping characters. Returns the smallest
    rotation count that gives the most coincidences
    :param cipher_text: Encrypted text
    :type cipher_text: str
    :return: Estimated key length
    """
    max_overlap = -1
    max_shift_count = -1

    ct_deque = collections.deque(cipher_text)

    for s in range(len(cipher_text) - 1):
        ct_deque.rotate(1)
        cur_overlap = 0
        for i, c in enumerate(cipher_text):
            if c == ct_deque[i]:
                cur_overlap += 1
        if cur_overlap > max_overlap:
            max_overlap = cur_overlap
            max_shift_count = s

    return max_shift_count
