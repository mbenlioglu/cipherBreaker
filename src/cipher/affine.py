"""
    Created by mbenlioglu on 10/3/2017
"""
from _cipher_utils import multiplicative_inverse


# ======================================================================================================================
# Public
# ======================================================================================================================
def encrypt(text, alpha, beta):
    """
    Encryption according to affine cipher with given alpha & beta values.
    :param text: Plain text to be encrypted. Only [A-Za-z] part of the text is encrypted
    :type text: str
    :param alpha: Alpha value of key in modulo 26
    :type alpha: int
    :param beta: Beta value of key in modulo 26
    :type beta: int
    :return: Encrypted cipher text
    """
    # parameter check
    if alpha not in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        raise ValueError('Invalid Alpha value! gcd(alpha,26) must be 1')
    if beta > 25:
        raise ValueError('Invalid Beta value! Must be between 0-26')

    cipher_text = list(text)
    for i, c in enumerate(text):
        if c.isupper():
            cipher_text[i] = chr((alpha * (ord(cipher_text[i]) - 65) + beta) % 26 + 65)
        elif c.islower():
            cipher_text[i] = chr((alpha * (ord(cipher_text[i]) - 97) + beta) % 26 + 97)

    return ''.join(cipher_text)


def decrypt(cipher_text, alpha, beta):
    """
    Reverse encryption operation for affine cipher
    :param cipher_text: Cipher text that is encrypted with affine cipher. Only [A-Za-z] part of the text is considered
    :type cipher_text: str
    :param alpha: Alpha value used for encryption in modulo 26
    :type alpha: int
    :param beta: Beta value used for encryption in modulo 26
    :type beta: int
    :return: Decrypted plain text result
    """
    # parameter check
    if alpha not in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        raise ValueError('Invalid Alpha Value! gcd(alpha, 26) must be 1')
    if beta > 25:
        raise ValueError('Invalid Beta value! Must be between 0-26')

    return encrypt(cipher_text, multiplicative_inverse(alpha, 26), 26 - beta)


def force_break(cipher_text, lang='en-us', method='brute', known_matches=None):
    """

    :param cipher_text:
    :param lang:
    :param method:
    :param known_matches:
    :return:
    """

# ======================================================================================================================
# Private
# ======================================================================================================================
