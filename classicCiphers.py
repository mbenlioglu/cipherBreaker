"""
    Created by mbenlioglu on 10/3/2017
"""
import argparse
from src.cipher import affine, caesar, vigenere
from src.strings import descriptions


def encrypt(args):
    if args.type == 'affine':
        if len(args.key) < 2:
            raise ValueError('2 int keys needed')
        print 'Encryption result: '
        print affine.encrypt(args.text, int(args.key[0]), int(args.key[-1]))
    elif args.type == 'caesar':
        print 'Encryption result: '
        print caesar.encrypt(args.text, int(args.key))
    elif args.type == 'vigenere':
        print 'Encryption result: '
        print vigenere.encrypt(args.text, args.key)


def decrypt(args):
    if args.type == 'affine':
        if len(args.key) < 2:
            raise ValueError('2 int keys needed')
        print 'Decryption result: '
        print affine.decrypt(args.text, int(args.key[0]), int(args.key[-1]))
    elif args.type == 'caesar':
        print 'Decryption result: '
        print caesar.decrypt(args.text, int(args.key))
    elif args.type == 'vigenere':
        print 'Decryption result: '
        print vigenere.decrypt(args.text, args.key)


def force_break(args):
    if args.type == 'affine':
        result = affine.force_break(args.text, args.lang, args.method, args.known)
        print 'Extracted alpha: ', result['alpha'], ', beta: ', result['beta']
        print 'Decrypted text: ', result['decrypted']
    elif args.type == 'caesar':
        result = caesar.force_break(args.text, args.lang, args.method)
        print 'Number of solutions found', len(result)
        for i in range(len(result)):
            print 'Shift amount: ', result[i]['shift'], 'Decrypted text:', result[i]['decrypted']
    elif args.type == 'vigenere':
        result = vigenere.force_break(args.text, args.lang)
        print 'Extracted passkey: ', result['passkey']
        print 'Decrypted text: ', result['decrypted']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=descriptions.intro,
                                     epilog=descriptions.examples,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(title=descriptions.subparser_title, description=descriptions.subparser_help)

    # parser for "encrypt"
    parser_enc = subparsers.add_parser('encrypt', help=descriptions.help_encrypt)
    parser_enc.add_argument('-t', '--type', help=descriptions.help_type, choices=descriptions.cipher_choices,
                            required=True)
    parser_enc.add_argument('--key', nargs='*', help=descriptions.help_key, required=True)
    parser_enc.add_argument('--text', help=descriptions.help_plain_text, required=True)
    parser_enc.set_defaults(func=encrypt)

    # parser for "decrypt"
    parser_dec = subparsers.add_parser('decrypt', help=descriptions.help_decrypt)
    parser_dec.add_argument('-t', '--type', help=descriptions.help_type, choices=descriptions.cipher_choices,
                            required=True)
    parser_dec.add_argument('--key', nargs='*', help=descriptions.help_key, required=True)
    parser_dec.add_argument('--text', help=descriptions.help_cipher_text, required=True)
    parser_dec.set_defaults(func=decrypt)

    # parser for "break"
    parser_brk = subparsers.add_parser('break', help=descriptions.help_break,
                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_brk.add_argument('-t', '--type', help=descriptions.help_type, choices=descriptions.cipher_choices,
                            required=True)
    parser_brk.add_argument('--text', help=descriptions.help_cipher_text, required=True)
    parser_brk.add_argument('--known', nargs=2, metavar=('original', 'encrypted'), action='append',
                            help=descriptions.help_known)
    parser_brk.add_argument('-l', '--lang', help=descriptions.help_lang, default='en_us')
    parser_brk.add_argument('-m', '--method', help=descriptions.help_method, choices=['brute', 'freq'], default='brute')
    parser_brk.set_defaults(func=force_break)

    args = parser.parse_args()
    args.func(args)
