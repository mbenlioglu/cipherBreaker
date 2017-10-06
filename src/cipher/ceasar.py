"""
    Created by mbenlioglu on 10/3/2017
"""
from ..strings import paths
from _cipher_utils import shift, monogram_frequency_analysis


# ======================================================================================================================
# Public
# ======================================================================================================================
def encrypt(text, amount):
    """
    Encryption with given shift amount
    :param text:  Plain text string to be encrypted with caesar cipher, spaces and special characters are ignored
    :type text: str
    :param amount: Amount of shift that is gonna be used to encrypt
    :type amount: int
    :return: Encrypted text
    """
    cipher_text = list(text)
    for i, c in enumerate(text):
        if c.isupper():
            cipher_text[i] = chr(shift(ord('A'), ord('Z'), ord(c), amount))
        elif c.islower():
            cipher_text[i] = chr(shift(ord('a'), ord('z'), ord(c), amount))

    return "".join(cipher_text)


def decrypt(cipher_text, amount):
    """
    Reverse encryption operation
    :param cipher_text: Cipher text string to be decrypted with caesar cipher, spaces and special characters are ignored
    :type cipher_text: str
    :param amount: Amount of shift that is gonna be used to decrypt
    :type amount: int
    :return: Decrypted text
    """
    return encrypt(cipher_text, -amount)


def force_break(cipher_text, lang='en-us', method='brute'):
    """
    Applies cipher-text only attack and tries to find decrypted text with either brute force or frequency analysis,
    which is defined in ":param method"
    :param cipher_text: Cipher text string to be decrypted, which is known to be encrypted with caesar cipher
    :type cipher_text: str
    :param lang: Language of original text default is 'en-us'
    :type lang: str
    :param method: Method of attack [ brute | freq ]. Default is brute
    :type method: str
    :return: Extracted all possible plain texts and their corresponding shift counts from cipher text
    """
    if method == 'brute':
        return _brute_force(cipher_text, lang)
    elif method == 'freq':
        frequency_result = monogram_frequency_analysis(cipher_text)
        return [{'shift': frequency_result['recommended'],
                 'decrypted': decrypt(cipher_text, frequency_result['recommended'])}]
    else:
        raise ValueError('Parameter method is not valid! (' + method + ')')


# ======================================================================================================================
# Private
# ======================================================================================================================
def _brute_force(cipher_text, lang='en-us'):
    """
    Try to find plain text possibilities from given encrypted text by trying all possibilities
    :param cipher_text: Encrypted text with caesar cipher (spaces and spacial characters are ignored)
    :type cipher_text: str
    :param lang: original language of the cipher text
    :type lang: str
    :return: List of possible plain text results and shift counts of corresponding results.
    """
    total_words = len(cipher_text.split())

    # load lookup table of words for language
    dict_name = lang + '_words'
    f = open(getattr(paths, dict_name), 'r')
    dictionary = frozenset(f.readlines())
    f.close()

    result = []
    for i in range(25):
        decrypted = decrypt(cipher_text, i).split()
        match_count = 0

        # check matching percentage of words in decrypted text
        for word in decrypted:
            if word in dictionary:
                match_count += 1

        # accept result if match rate is over 90%
        if float(match_count) / total_words >= 0.9:
            result.append({'shift': i, 'decrypted': ''.join(decrypted)})

    return result
