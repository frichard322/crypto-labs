from random import choices
from string import ascii_letters, digits, punctuation

from solitaire import Solitaire

s = Solitaire()
i: int = 0
k: int = 5


def test(msg: str):
	global i, k
	print(f"{i}.Test:")
	print("Message:", msg)
	key = s.generate_key(i*k, (i+1)*k)
	e_msg = Solitaire.crypt(msg, key)
	print("Encrypted:", e_msg)
	# Offset manipulation makes it fail
	# key = s.generate_key(i*k+1, (i+1)*k)
	d_msg = Solitaire.crypt(e_msg, key)
	print("Decrypted:", d_msg)
	i += 1
	if msg != d_msg:
		raise "Cypher failed: message != decrypted message"


def main():
	global k
	for _ in range(25):
		chars = ascii_letters + digits + punctuation
		msg = "".join(choices(chars, k=k))
		test(msg)


if __name__ == '__main__':
	main()
