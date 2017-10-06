# cipherBreaker
Encryption, decryption and breaking tool for classical ciphers

**Implemented by:**
 * [M.Mucahid Benlioglu](https://github.com/mbenlioglu)

## Getting started
In order to use cipher encryption, decryption and breaking you need to run /classicCiphers.py with the following
instructions.

Note that this project is written and tested under [Python 2.7.x](https://docs.python.org/2/)

### Usage:

**General:**

    classicCiphers.py [-h] {encrypt,decrypt,break} ...
    
    Encryption, decryption and breaking tool for classical ciphers
    
    optional arguments:
      -h, --help            show this help message and exit
    
    Available operations:
      Execute "classicCiphers.py {subcommand} --help" for more information about each of
      these subcommands
    
      {encrypt,decrypt,break}
        encrypt             Performs encryption with chosen cipher type and
                            parameters
        decrypt             Performs decryption with chosen cipher type and
                            parameters
        break               Tries to reach the plain text from encrypted according
                            to cipher type using given parameters
    
    Examples:
    -----------
    
    python classicCiphers.py break -t caesar --text XJGY
    python classicCiphers.py break -t affine --text "HR JNAF" --known R O
    python classicCiphers.py decrypt -t vigemere --text WZWR --key SESAME

**Encryption:**

    classicCiphers.py encrypt [-h] -t {affine,caesar,vigenere} --key KEY
                                     --text TEXT
    
    optional arguments:
      -h, --help            show this help message and exit
      -t {affine,caesar,vigenere}, --type {affine,caesar,vigenere}
                            Type of the Classical cipher
      --key KEY             Passkey or Shift amount(s) to be used as
                            encryption/decryption key.
      --text TEXT           Plain text to be encrypted

**Decryption:**

    classicCiphers.py decrypt [-h] -t {affine,caesar,vigenere} --key KEY
                                     --text TEXT
    
    optional arguments:
      -h, --help            show this help message and exit
      -t {affine,caesar,vigenere}, --type {affine,caesar,vigenere}
                            Type of the Classical cipher
      --key KEY             Passkey or Shift amount(s) to be used as
                            encryption/decryption key.
      --text TEXT           Cipher text to be decrypted

**Breaking:**

    classicCiphers.py break [-h] -t {affine,caesar,vigenere} --text TEXT
                                   [--known original encrypted]
    
    optional arguments:
      -h, --help            show this help message and exit
      -t {affine,caesar,vigenere}, --type {affine,caesar,vigenere}
                            Type of the Classical cipher
      --text TEXT           Cipher text to be decrypted
      --known original encrypted
                            Known original-encrypted character pairs to make it
                            easier to break
   
