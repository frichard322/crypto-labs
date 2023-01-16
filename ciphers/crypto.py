#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Kriptografia (2021-2022)
Course: Klasszikus kriptorendszerek
Name: Farago Richard
SUNet: frim1910
"""
from math import ceil, floor
import nltk


# Caesar Cipher

def encrypt_caesar(plaintext):
	return "".join(map(lambda c: chr((ord(c) - ord("A") + 3) % 26 + ord("A")) if ord(c) in range(65, 90) else c, list(plaintext)))


def decrypt_caesar(ciphertext):
	return "".join(map(lambda c: chr((ord(c) - ord("A") - 3) % 26 + ord("A")) if ord(c) in range(65, 90) else c, list(ciphertext)))


# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
	keyword *= ceil(len(plaintext) / len(keyword))
	keyword = keyword[0:len(plaintext)]
	return "".join(map(lambda c: chr((ord(c[0]) - ord("A") + ord(c[1]) - ord("A")) % 26 + ord("A")) if ord(c[0]) in range(65, 91) else c[0], zip(list(plaintext), list(keyword))))


def decrypt_vigenere(ciphertext, keyword):
	keyword *= ceil(len(ciphertext) / len(keyword))
	keyword = keyword[0:len(ciphertext)]
	return "".join(map(lambda c: chr((ord(c[0]) - ord("A") - ord(c[1]) - ord("A")) % 26 + ord("A")) if ord(c[0]) in range(65, 91) else c[0], zip(list(ciphertext), list(keyword))))


# Scytale Cipher

def encrypt_scytale(plaintext, circumference):
	if not isinstance(circumference, int):
		circumference = int(circumference)
	lines = ["" for _ in range(circumference)]
	for i, c in enumerate(plaintext):
		lines[i % circumference] += c
	return "".join(lines)


def decrypt_scytale(ciphertext, circumference):
	if not isinstance(circumference, int):
		circumference = int(circumference)
	return encrypt_scytale(ciphertext, floor(len(ciphertext)/circumference))


# Railfence Cipher

def encrypt_railfence(plaintext, num_rails):
	if not isinstance(num_rails, int):
		num_rails = int(num_rails)
	lines = [[] for _ in range(num_rails)]
	pattern = [*range(num_rails - 1), *range(num_rails - 1, 0, -1)]
	# for debug purpose
	# print(pattern)
	for i, c in enumerate(plaintext):
		lines[pattern[i % len(pattern)]].append(c)
	return [char for sublist in lines for char in sublist]


def decrypt_railfence(ciphertext, num_rails):
	if not isinstance(num_rails, int):
		num_rails = int(num_rails)
	numbers = [str(i) for i in range(len(ciphertext))]
	positions = encrypt_railfence(numbers, num_rails)
	# for debug purpose
	# print(f"numbers({len(numbers)}): {numbers}")
	# print(f"positions({len(positions)}): {positions}")
	# print(f"ciphertext({len(ciphertext)}): {ciphertext}")
	return [ciphertext[positions.index(i)] for i in numbers]


def decrypt_vigenere_codebreaker(ciphertext, possible_keys):
	max_percentage = 0.0
	max_word = None
	max_plaintext = None
	for word in possible_keys:
		plaintext = decrypt_vigenere(ciphertext, word)
		list_of_words = [word for word in nltk.word_tokenize(plaintext) if word.isalpha()]
		english_words = filter(lambda w: True if w in possible_keys else False, list_of_words)
		percentage = len(list(english_words)) / len(list_of_words)
		if percentage > max_percentage:
			max_percentage = percentage
			max_word = word
			max_plaintext = plaintext

	return max_plaintext, max_word, max_percentage
