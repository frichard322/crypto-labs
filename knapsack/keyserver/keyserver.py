from json import loads, dumps
from socket import socket, AF_INET, SOCK_DGRAM


class KeyServer(socket):
	def __init__(self):
		super().__init__(family=AF_INET, type=SOCK_DGRAM)
		self.bind(("localhost", 8000))
		self.key_dict: dict[int, tuple[int]] = {}
		self._start_listening()

	def _exists_id(self, client_id: int) -> bool:
		return client_id in self.key_dict.keys()

	def _update_key(self, client_id: int, public_key: tuple[int]):
		self.key_dict[client_id] = public_key

	def _start_listening(self) -> None:
		while True:
			outgoing: dict[str, any] = {}
			data, address = self.recvfrom(10240)
			incoming: dict[str, any] = loads(data)
			print("Incoming from", address, ", body:", incoming)
			if not isinstance(incoming, dict):
				outgoing["message"] = "Please provide a valid json format!"
				outgoing["error"] = 1
			elif "client_id" not in incoming.keys():
				outgoing["message"] = "Please provide a client id!"
				outgoing["error"] = 1
			elif "public_key" not in incoming.keys():
				if not isinstance(incoming["client_id"], int):
					outgoing["message"] = "Please provide a valid client id (integer)!"
					outgoing["error"] = 1
				elif not self._exists_id(incoming["client_id"]):
					outgoing["message"] = "Please provide a public key for registration or update!"
					outgoing["error"] = 1
				else:
					outgoing["message"] = "Public key sent!"
					outgoing["public_key"] = self.key_dict[incoming["client_id"]]
			else:
				if not isinstance(incoming["public_key"], list) or len(incoming["public_key"]) != 8:
					outgoing["message"] = "Please provide a valid public key (list/tuple, size of 8)!"
					outgoing["error"] = 1
				else:
					if not self._exists_id(incoming["client_id"]):
						outgoing["message"] = "Public key added!"
					else:
						outgoing["message"] = "Public key updated!"
					self._update_key(incoming["client_id"], incoming["public_key"])
			print("Outgoing to", address, ", body:", outgoing)
			self.sendto(dumps(outgoing).encode("ascii"), address)


if __name__ == '__main__':
	KeyServer()
