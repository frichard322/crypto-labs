#!/usr/bin/env python3 -tt
"""
File: crypto-console.py
-----------------------
Implements a console menu to interact with the cryptography functions exported
by the crypto module.

If you are a student, you shouldn't need to change anything in this file.
"""
import base64

from assign1.utils import byte_to_bits, bits_to_byte
from crypto import (encrypt_caesar, decrypt_caesar,
                    encrypt_vigenere, decrypt_vigenere,
                    encrypt_scytale, decrypt_scytale,
                    encrypt_railfence, decrypt_railfence)


#############################
# GENERAL CONSOLE UTILITIES #
#############################

def get_tool():
    print("* Tool *")
    return _get_selection("(C)aesar, (V)igenere, (S)cytale or (R)ailfence? ", "CVSR")


def get_action():
    """Return true if encrypt"""
    print("* Action *")
    return _get_selection("(E)ncrypt or (D)ecrypt? ", "ED")


def get_binary():
    """Return true if binary"""
    print("* Binary *")
    return _get_selection("(B)inary or (A)scii? ", "BA")


def get_filename():
    filename = input("Filename? ")
    while not filename:
        filename = input("Filename? ")
    return filename


def get_input(binary=False):
    print("* Input *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        text = input("Enter a string: ").strip().upper()
        while not text:
            text = input("Enter a string: ").strip().upper()
        if binary:
            return bytes(text, encoding='utf8')
        return text
    else:
        filename = get_filename()
        flags = 'r'
        if binary:
            flags += 'b'
        with open(filename, flags) as infile:
            return infile.read()


def set_output(output, binary=False):
    print("* Output *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        print(output)
    else:
        filename = get_filename()
        flags = 'w'
        if binary:
            flags += 'b'
        with open(filename, flags) as outfile:
            print("Writing data to {}...".format(filename))
            outfile.write(output)


def _get_selection(prompt, options):
    choice = input(prompt).upper()
    while not choice or choice[0] not in options:
        choice = input("Please enter one of {}. {}".format('/'.join(options), prompt)).upper()
    return choice[0]


def get_yes_or_no(prompt, reprompt=None):
    """
    Asks the user whether they would like to continue.
    Responses that begin with a `Y` return True. (case-insensitively)
    Responses that begin with a `N` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """
    if not reprompt:
        reprompt = prompt

    choice = input("{} (Y/N) ".format(prompt)).upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. {} (Y/N)? ".format(reprompt)).upper()
    return choice[0] == 'Y'


def clean_caesar(text):
    """Convert text to a form compatible with the preconditions imposed by Caesar cipher"""
    return text.upper()


def clean_vigenere(text):
    return ''.join(ch for ch in text.upper() if ch.isupper())


def clean_scytale(text):
    return ''.join(ch for ch in text.upper() if ch.isupper())


def clean_railfence(text):
    return ''.join(ch for ch in text.upper() if ch.isupper())


def run_caesar():
    action = get_action()
    encrypting = action == 'E'
    data = clean_caesar(get_input(binary=False))

    print("* Transform *")
    print("{}crypting {} using Caesar cipher...".format('En' if encrypting else 'De', data))

    output = (encrypt_caesar if encrypting else decrypt_caesar)(data)

    set_output(output)


def run_vigenere():
    action = get_action()
    encrypting = action == 'E'
    data = clean_vigenere(get_input(binary=False))

    print("* Transform *")
    keyword = clean_vigenere(input("Keyword? "))

    print("{}crypting {} using Vigenere cipher and keyword {}...".format('En' if encrypting else 'De', data, keyword))

    output = (encrypt_vigenere if encrypting else decrypt_vigenere)(data, keyword)

    set_output(output)


def run_scytale():
    action = get_action()
    encrypting = action == 'E'
    data = clean_scytale(get_input(binary=False))

    print("* Transform *")
    circumference = clean_scytale(input("Circumference of? "))
    while not circumference.isnumeric():
        circumference = input("The provided input is not a number, try again! Circumference of? ")

    print(
        "{}crypting {} using Scytale cipher and circumference of {}...".format('En' if encrypting else 'De', data, circumference))

    output = (encrypt_scytale if encrypting else decrypt_scytale)(data, circumference)

    set_output(output)


def run_railfence():
    action = get_action()
    encrypting = action == 'E'
    binary = get_binary() == 'B'
    if binary is True:
        input_ = bytes(get_input(binary))
        data = [byte_to_bits(byte) for byte in input_]
    else:
        input_ = get_input(binary)
        data = clean_railfence(input_)

    print("* Transform *")
    num_rails = input("Number of rails? ")
    while not num_rails.isnumeric():
        num_rails = input("The provided input is not a number, try again! Number of rails? ")

    if binary is True:
        print("{}crypting binary file using Railfence cipher and number of rails {}...".format('En' if encrypting else 'De', num_rails))
    else:
        print("{}crypting {} using Railfence cipher and number of rails {}...".format('En' if encrypting else 'De', data, num_rails))

    output = (encrypt_railfence if encrypting else decrypt_railfence)(data, num_rails)

    if binary is True:
        set_output(bytearray([bits_to_byte(bits) for bits in output]), binary)
    else:
        set_output("".join(output))


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print('-' * 34)
    tool = get_tool()
    # This isn't the cleanest way to implement functional control flow,
    # but I thought it was too cool to not sneak in here!
    commands = {
        'C': run_caesar,         # Caesar Cipher
        'V': run_vigenere,       # Vigenere Cipher
        'S': run_scytale,        # Scytale Cipher
        'R': run_railfence,      # Railfence Cipher
    }
    commands[tool]()


def main():
    """Harness for CS41 Assignment 1"""
    print("Welcome to the Cryptography Suite!")
    run_suite()
    while get_yes_or_no("Again?"):
        run_suite()
    print("Goodbye!")


if __name__ == '__main__':
    main()
