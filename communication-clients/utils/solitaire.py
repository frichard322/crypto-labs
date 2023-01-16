def shuffle(key: str) -> list[str]:
	shuffled = [str(x) if 0 <= x < 26 else "A" if x == 26 else "B" for x in [ord(c) % 28 for c in key]]
	return shuffled


# Reference: https://en.wikipedia.org/wiki/Solitaire_(cipher)
def solitaire(key: str, length: int) -> str:
	deck = shuffle(key)

	key = []

	for _ in range(length):
		byte = 0
		steps = 0
		while steps < 2:
			# Locate both jokers
			index1 = deck.index("A")
			index2 = deck.index("B")
			if index1 > index2:
				index1, index2 = index2, index1
			# Move the first by one
			new_index = (index1 + 1) % 28
			if new_index == 0:
				new_index += 1
			deck[index1], deck[new_index] = deck[new_index], deck[index1]
			# Move the second by two
			new_index = (index2 + 2) % 28
			if new_index == 0 or new_index == 1:
				new_index += 1
			deck[index2], deck[new_index] = deck[new_index], deck[index2]
			# Perform a triple cut
			deck = [*deck[index2:], *deck[index1-1:index2], *deck[:index1-1]]
			# Perform a count cut
			value = deck[-1]
			if value != "A" and value != "B":
				value = int(value)
				deck = [*deck[value:-1], *deck[:value], deck[-1]]
			# Get the top value which is the next in the key stream
			if deck[0] != "A" and deck[0] != "B":
				steps += 1
				x = deck[int(deck[0])]
				if x == "A":
					x = 26
				elif x == "B":
					x = 27
				else:
					x = int(x)
				byte += x % 16
				if steps == 1:
					byte = byte << 4
		key.append(chr(byte))
	return "".join(key)
