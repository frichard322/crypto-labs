from assign1.utils import is_superincreasing, coprime, modinv, byte_to_bits
from random import randint


class MerkleHellman(object):
	@staticmethod
	def generate_private_key(n: int = 8) -> tuple[tuple[int], int, int]:
		"""Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem

        Following the instructions in the handout, construct the private key components
        of the MH Cryptosystem. This consistutes 3 tasks:

        1. Build a superincreasing sequence `w` of length n
            (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
        2. Choose some integer `q` greater than the sum of all elements in `w`
        3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

        You'll need to use the random module for this function, which has been imported already

        Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

        @param n bitsize of message to send (default 8)
        @type n int

        @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
        """
		l: list[int] = [randint(2, 10)]
		total: int = sum(l)
		for i in range(1, n + 1):
			r: int = randint(total + 1, 2 * total)
			l.append(r)
			total += r
		if not is_superincreasing(l):
			raise Exception("Not super-increasing sequence!")

		w: tuple[int] = tuple(l[:n])
		q: int = l[n]

		r: int = 0
		while not coprime(q, r):
			r = randint(2, q - 1)

		return w, q, r

	@staticmethod
	def create_public_key(private_key: tuple[tuple[int], int, int]) -> tuple[int]:
		"""Creates a public key corresponding to the given private key.

        To accomplish this, you only need to build and return `beta` as described in the handout.

            beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

        Hint: this can be written in one line using a list comprehension

        @param private_key The private key
        @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

        @return n-tuple public key
        """
		return tuple([private_key[2] * w % private_key[1] for w in private_key[0]])

	@staticmethod
	def encrypt_mh(message: str, public_key: tuple[int]) -> str:
		"""Encrypt an outgoing message using a public key.
            (X - represents skipped tasks, there was no need to chunk the message)
        X 1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
        X 2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
        3. Encrypt the 8 message bits by computing
             c = sum of a_i * b_i for i = 1 to n
        4. Return a list of the encrypted ciphertexts for each chunk in the message

        Hint: think about using `zip` at some point

        @param message The message to be encrypted
        @type message bytes
        @param public_key The public key of the desired recipient
        @type public_key n-tuple of ints

        @return string representing encrypted bytes
        """
		return "".join([chr(sum([a * b for a, b in list(zip(byte_to_bits(ord(alpha)), public_key))])) for char in message for alpha in char])

	@staticmethod
	def decrypt_mh(message: str, private_key: tuple[tuple[int], int, int]) -> str:
		"""Decrypt an incoming message using a private key

        1. Extract w, q, and r from the private key
        2. Compute s, the modular inverse of r mod q, using the
            Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
        3. For each byte-sized chunk, compute
             c' = cs (mod q)
        4. Solve the superincreasing subset sum using c' and w to recover the original byte
        5. Reconsitite the encrypted bytes to get the original message back

        @param message Encrypted message chunks
        @type message list of ints
        @param private_key The private key of the recipient
        @type private_key 3-tuple of w, q, and r

        @return bytearray or str of decrypted characters
        """
		w, q, r = private_key
		s = modinv(r, q)
		c = [(ord(char) * s) % q for char in message]
		text: list[chr] = []
		for cc in c:
			new_char: int = 0
			for i in range(7, -1, -1):
				if cc >= w[i]:
					cc -= w[i]
					new_char |= (1 << (7 - i))
				if cc == 0:
					break
			text.append(chr(new_char))

		return "".join(text)


mh = MerkleHellman()
