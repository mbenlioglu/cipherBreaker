"""
    Created by mbenlioglu on 10/3/2017
"""
import collections
from _cipher_utils import shift, get_letter_num
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


def force_break(cipher_text):
    """
    Applies frequency analysis of overlapping letters with cipher text and rotated versions of it to guess passkey
    length, from there cipher text is broken into smaller shift ciphers and plain text is guessed through applying
    monogram frequency analysis.
    :param cipher_text: Encrypted text using Vinegere cipher
    :type cipher_text: str
    :return: Extracted passkey and plain text from the encrypted text
    """
    key_length = _passkey_length_guess(cipher_text)
    sub_ciphers = [cipher_text[i::key_length] for i in range(key_length)]

    resolved = []
    passkey = []
    for sub in sub_ciphers:
        caesar_result = caesar.force_break(''.join(sub), method='freq')
        passkey.append(chr(caesar_result[0]['shift'] + 65))
        resolved.append(caesar_result[0]['decrypted'])

    return {'passkey': ''.join(passkey), 'decrypted': ''.join([c for l in zip(*resolved) for c in l])}


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

    cipher_no_space = ''.join(cipher_text.split())
    ct_deque = collections.deque(cipher_no_space)

    for s in range(len(cipher_no_space) - 1):
        ct_deque.rotate(1)
        cur_overlap = 0
        for i, c in enumerate(cipher_no_space):
            if c == ct_deque[i]:
                cur_overlap += 1
        if cur_overlap > max_overlap:
            max_overlap = cur_overlap
            max_shift_count = s

    return max_shift_count
