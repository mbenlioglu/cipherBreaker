"""
    Created by mbenlioglu on 10/3/2017
"""
from _cipher_utils import multiplicative_inverse, get_letter_num
from src.strings import paths


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
    Applies cipher-text only attack and tries to find decrypted text with either brute force or frequency analysis,
    which is defined in ":param method"
    :param cipher_text: Cipher text string to be decrypted, which is known to be encrypted with affine cipher
    :type cipher_text: str
    :param lang: Language of original text default is 'en-us'
    :type lang: str
    :param method: Method of attack [ brute | freq ]. Default is brute
    :type method: str
    :param known_matches: List of tuples, where each tuple contains a pair of plain text - cipher text matches, more
    precisely [(<ORIGINAL LETTER>, <ENCRYPTED LETTER>), (...)]
    :type known_matches: list of (str, str)
    :return: Decrypted string with corresponding alpha, beta values
    """
    if method == 'brute':
        # load lookup table of words for language
        # dict_name = lang + '_words'
        f = open(paths.en_us_words, 'r')
        word_set = frozenset(x.upper() for x in f.read().splitlines())
        f.close()

        alphas = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
        if known_matches is None:
            for alpha in alphas:
                for beta in range(26):
                    result = _decrypt_and_check(cipher_text, alpha, beta, word_set)

                    # accept result if match rate is over 90%
                    if result['match_rate'] >= 0.9:
                        return {'alpha': alpha, 'beta': beta, 'decrypted': result['decrypted']}
        elif len(known_matches) == 1:
            # only use (alpha, beta) keys that satisfy the equation: alpha * t + beta = c mod 26
            for alpha in alphas:
                for beta in range(26):
                    if (alpha * get_letter_num(known_matches[0][0]) + beta) % 26 == get_letter_num(known_matches[0][1]):
                        result = _decrypt_and_check(cipher_text, alpha, beta, word_set)

                        # accept result if match rate is over 90%
                        if result['match_rate'] >= 0.9:
                            return {'alpha': alpha, 'beta': beta, 'decrypted': result['decrypted']}
        else:
            # determine alpha and beta, return result
            org1 = known_matches[0][0]
            org2 = known_matches[1][0]
            cip1 = known_matches[0][1]
            cip2 = known_matches[1][1]

            alpha = (get_letter_num(cip1) - get_letter_num(cip2)) % 26
            alpha *= multiplicative_inverse((get_letter_num(org1) - get_letter_num(org2)) % 26, 26)

            beta = (get_letter_num(cip1) - alpha * get_letter_num(org1)) % 26
            return {'alpha': alpha, 'beta': beta, 'decrypted': decrypt(cipher_text, alpha, beta)}
    elif method == 'freq':
        raise NotImplementedError  # todo later on
    else:
        raise ValueError('Parameter method is not valid! (' + method + ')')


# ======================================================================================================================
# Private
# ======================================================================================================================
def _decrypt_and_check(cipher_text, alpha, beta, word_set):
    """
    Decrypts using given alpha & beta and calculates the match rate of result
    :param cipher_text: Cipher text that is encrypted with affine cipher. Only [A-Za-z] part of the text is considered
    :type cipher_text: str
    :param alpha: Alpha value used for encryption in modulo 26
    :type alpha: int
    :param beta: Beta value used for encryption in modulo 26
    :type beta: int
    :param word_set: Set of natural words for decryption results to be compared with
    :return: Decryption result and corresponding word mathch rate
    """
    match_count = 0
    total_words = len(cipher_text.split())
    decrypted = decrypt(cipher_text, alpha, beta).split()

    # check matching percentage of words in decrypted text
    for word in decrypted:
        if word.upper() in word_set:
            match_count += 1

    return {'match_rate': float(match_count) / total_words, 'decrypted': ''.join(decrypted)}
