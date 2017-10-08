"""
    Created by mbenlioglu on 10/5/2017
"""

# general explanations
intro = 'Encryption, decryption and breaking tool for classical ciphers'
examples = '''\
Examples:
-----------

python %(prog)s break -t caesar --text XJGY
python %(prog)s break -t affine --text "HR JNAF" --known R O
python %(prog)s decrypt -t vigemere --text WZWR --key SESAME

'''
cipher_choices = ['affine', 'caesar', 'vigenere']

# subparsers general help
subparser_title = 'Available operations'
subparser_help = 'Execute "%(prog)s {subcommand} --help" for more information about each of these subcommands'

# common
help_plain_text = 'Plain text to be encrypted'
help_cipher_text = 'Cipher text to be decrypted'
help_key = 'Passkey or Shift amount(s) to be used as encryption/decryption key.'
help_type = 'Type of the Classical cipher'
help_known = 'Known original-encrypted character pairs to make it easier to break'
help_method = 'Method to be used for breaking cipher. Ignored in vigenere.'
help_lang = 'Language of the original plain text in 4 letter code form'

# subcommand specific
help_encrypt = 'Performs encryption with chosen cipher type and parameters'
help_decrypt = 'Performs decryption with chosen cipher type and parameters'
help_break = 'Tries to reach the plain text from encrypted according to cipher type using given parameters'
