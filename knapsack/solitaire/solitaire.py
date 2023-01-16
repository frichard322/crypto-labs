from random import shuffle

from assign1.utils import bits_to_byte, byte_to_bits


class Solitaire(object):
	def __init__(self, deck: list[int] = None):
		if deck is None:
			self.deck = list(range(28))
			shuffle(self.deck)
		else:
			self.deck = deck
		self.key: list[chr] = []

	def generate_key(self, start: int, end: int) -> str:
		length = end - len(self.key)
		if length > 0:
			for _ in range(length):
				byte = 0
				steps = 0
				while steps < 2:
					# Locate both jokers
					index1 = self.deck.index(26)
					index2 = self.deck.index(27)
					if index1 > index2:
						index1, index2 = index2, index1
					# 1.Move the first by one
					new_index = (index1 + 1) % 28
					self.deck[index1], self.deck[new_index] = self.deck[new_index], self.deck[index1]
					index1 = new_index
					# 2.Move the second by two
					new_index = (index2 + 2) % 28
					self.deck[index2], self.deck[new_index] = self.deck[new_index], self.deck[index2]
					index2 = new_index
					# 3.Perform a triple cut
					self.deck = [*self.deck[index2+1:], *self.deck[index1:index2+1], *self.deck[:index1]]
					# 4.Perform a count cut
					value = self.deck[-1]
					if value == 27:
						value = 26
					self.deck = [*self.deck[value:-1], *self.deck[:value], self.deck[-1]]
					# 5.Get the top value which is the next in the key stream
					value = self.deck[0]
					if value == 27:
						value = 26
					x = self.deck[value + 1]
					if x != 26 and x != 27:
						steps += 1
						byte += x % 16
						if steps == 1:
							byte = byte << 4
				self.key.append(chr(byte))
		return "".join(self.key[start:end])

	@staticmethod
	def crypt(msg: str, key: str) -> str:
		return "".join([chr(bits_to_byte([bit1 ^ bit2 for bit1, bit2 in list(zip(x, y))])) for x, y in [(byte_to_bits(ord(byte1)), byte_to_bits(ord(byte2))) for byte1, byte2 in list(zip(msg, key))]])
