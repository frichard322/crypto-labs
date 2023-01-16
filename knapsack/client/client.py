from sys import exit
from json import dumps, loads
from random import shuffle
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread, Lock
from time import sleep

from knapsack.merklehellman.merklehellman import mh
from knapsack.solitaire import Solitaire


class Client(socket):
	# Used for synchronously logging messages
	lock = Lock()

	def __init__(self, port: int, partner_port: int):
		super().__init__(family=AF_INET, type=SOCK_DGRAM)
		self.partner = ((), partner_port)
		self.address = ("localhost", port)
		self.bind(self.address)
		self._initialize()
		self.deck: list[int] = []
		self._build_solitaire_deck()
		self.solitaire: Solitaire = Solitaire(self.deck)
		Listener(self).start()
		self._start_publishing()

	"""
		- Encrypts message with MH public key
	"""
	def _encrypt_mh(self, message: str) -> str:
		return mh.encrypt_mh(message, self.partner[0])

	"""
		- Decrypts message with MH private key
	"""
	def _decrypt_mh(self, message: str) -> str:
		return mh.decrypt_mh(message, self.private_key)

	"""
		- Generates private and public key
		- Registers its key to the key-server
		- Gets other client's public key from key-server
	"""
	def _initialize(self):
		# Generating keys
		self.log(2, f"Generating keys...")
		self.private_key = mh.generate_private_key()
		self.public_key = mh.create_public_key(self.private_key)
		self.log(2, f"Private key = {self.private_key}, Public key = {self.public_key}")

		# Register
		self.log(2, "Registering...")
		self.publish(
			8000,
			{
				"client_id": self.address[1],
				"public_key": self.public_key
			}
		)
		body, address = self.receive()
		self.log(0, body, address[1])
		input("Press any key when your partner is also ready...")

		# Get partner's public key
		self.publish(
			8000,
			{
				"client_id": self.partner[1],
			}
		)
		body, address = self.receive()
		self.log(0, body, address[1])
		if "public_key" in body.keys():
			self.partner = (body["public_key"], self.partner[1])
			self.log(2, f'Set partner public key to {body["public_key"]}')

		# Send hello encrypted to your partner
		sleep(5.0)
		if self.address[1] % 2 == 0:
			body, address = self.receive()
			self.log(0, self._decrypt_mh(body["message"]), address[1])
		self.publish(self.partner[1], {"message": mh.encrypt_mh("Hello", self.partner[0])})
		self.log(1, self._encrypt_mh("Hello"), self.partner[1])
		if self.address[1] % 2 == 1:
			body, address = self.receive()
			self.log(0, self._decrypt_mh(body["message"]), address[1])

	"""
		- Generates half deck depending on a set which contains cards that cannot be used anymore
	"""
	@staticmethod
	def _generate_half_deck(cards: set[int]):
		deck = list(range(28))
		shuffle(deck)
		if len(cards) == 0:
			return deck[:14]
		else:
			return [card for card in deck if card not in cards]

	"""
		- Converts deck to string
	"""
	@staticmethod
	def _convert_deck_to_string(deck: list[int]) -> str:
		return "".join([chr(card) for card in deck])

	"""
		- Converts string to deck
	"""
	@staticmethod
	def _convert_string_to_deck(string: str) -> list[int]:
		return [ord(char) for char in string]

	"""
		- Build solitaire deck
	"""
	def _build_solitaire_deck(self):
		cards: set[int] = set()
		# Generate half deck
		self.log(2, "Generating half deck...")
		# 1. Client
		if self.address[1] % 8000 == 1:
			half_deck1 = self._generate_half_deck(cards)
			self.log(1, f"Half deck = {half_deck1}", self.partner[1])
			self.publish(self.partner[1], {"half_deck": self._encrypt_mh(self._convert_deck_to_string(half_deck1))})
			body, address = self.receive()
			half_deck2 = self._convert_string_to_deck(self._decrypt_mh(body["half_deck"]))
			self.log(0, f'Half deck = {half_deck2}', address[1])
		# 2. Client
		else:
			body, address = self.receive()
			half_deck1 = self._convert_string_to_deck(self._decrypt_mh(body["half_deck"]))
			self.log(0, f'Half deck = {half_deck1}', address[1])
			[cards.add(card) for card in half_deck1]
			half_deck2 = self._generate_half_deck(cards)
			self.log(1, f"Half deck = {half_deck2}", self.partner[1])
			self.publish(self.partner[1], {"half_deck": self._encrypt_mh(self._convert_deck_to_string(half_deck2))})
		self.deck = [*half_deck1, *half_deck2]

	"""
		- Sends a `body` to `port`
	"""
	def publish(self, port: int, body: dict[str, any]):
		self.sendto(dumps(body).encode("UTF-8"), ("localhost", port))

	"""
		- Receives a `body` and forwards it as dictionary + address
	"""
	def receive(self, size: int = 1024) -> tuple[dict[str, any], tuple[str, int]]:
		data, address = self.recvfrom(size)
		body: dict[str, any] = loads(data)
		return body, address

	"""
		- Synchronously logs messages
		- Operations: (0 = receive, 1 = publish, X = self-operation)
	"""
	def log(self, operation: int, message: (dict[str, any], str), to_from: int = 0):
		if operation == 0:
			output = f'{self.address[1]} Client receives from {to_from}: {message}'
		elif operation == 1:
			output = f'{self.address[1]} Client publishes to {to_from}: {message}'
		else:
			output = f'{self.address[1]} Client: {message}'
		self.lock.acquire()
		print(output)
		self.lock.release()

	"""
		- Encrypts/Decrypts message with Solitaire
	"""
	def crypt_solitaire(self, message: str, start: int, end: int) -> str:
		return self.solitaire.crypt(message, self.solitaire.generate_key(start, end))

	"""
		- Start sending messages on input
	"""
	def _start_publishing(self):
		offset = 0
		while True:
			message = input()
			body = {
				"offset": {
					"start": offset,
					"end": offset + len(message)
				},
				"message": self.crypt_solitaire(message, offset, offset + len(message))
			}
			self.log(1, body, self.partner[1])
			self.publish(self.partner[1], body)
			if message == "BYE":
				break


class Listener(Thread):
	def __init__(self, client: Client):
		super().__init__()
		self.client = client

	def run(self) -> None:
		while True:
			body, address = self.client.receive()
			body["message"] = self.client.crypt_solitaire(body["message"], body["offset"]["start"], body["offset"]["end"])
			self.client.log(0, body, address[1])
			if body["message"] == "BYE":
				break
