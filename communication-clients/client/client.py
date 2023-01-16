from json import dumps, loads
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from time import sleep

from assign2.streamcipher import StreamCipher
from assign2.utils.blum_blum_shub import blum_blum_shub
from assign2.utils.config import KEY, SEED, GEN_TYPE
from assign2.utils.solitaire import solitaire


class Client(socket):
	print_locker = 0

	def __init__(self, port: int, name: str):
		super().__init__(family=AF_INET, type=SOCK_DGRAM)
		self.name = name
		self._offset = 0
		self._configure_cipher()
		self.bind(("localhost", port))
		self.listener_thread = Listener(self)

	def _configure_cipher(self) -> None:
		if GEN_TYPE == "solitaire":
			self.stream_cipher = StreamCipher(solitaire, key=KEY)
		else:
			# GEN_TYPE == "blum-blum-shub"
			self.stream_cipher = StreamCipher(blum_blum_shub, key=SEED)

	def lock(self) -> None:
		while self.print_locker:
			sleep(1)
		self.print_locker = 1

	def unlock(self) -> None:
		self.print_locker = 0

	def send_message(self, port: int, body: dict[str, any]) -> None:
		body["offset"] = self._offset
		if "text" in body.keys() and body["text"]:
			body = self.stream_cipher.crypt(body)
			self.lock()
			print("(", self.name, ")", "Sent:", body["text"])
			self.unlock()
			self._offset = len(body["text"])
		encode = dumps(body).encode("ascii")
		self.sendto(encode, ("localhost", port))

	def start_listening(self) -> None:
		self.listener_thread.start()


class Listener(Thread):
	def __init__(self, client: Client):
		super().__init__()
		self.client = client

	def run(self) -> None:
		while True:
			body: dict[str, any] = loads(self.client.recv(10240))
			if "text" in body.keys() and body["text"]:
				body = self.client.stream_cipher.crypt(body)
				self.client.lock()
				print("(", self.client.name, ")", "Received:", body["text"])
				self.client.unlock()
			if "stop" in body.keys() and body["stop"]:
				break
