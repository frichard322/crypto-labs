from json import dumps, loads
from socket import socket, AF_INET, SOCK_DGRAM


class TestClient(socket):
	print_locker = 0

	def __init__(self):
		super().__init__(family=AF_INET, type=SOCK_DGRAM)
		self.bind(("localhost", 7999))
		self.test(
			[
				"asd",
				{},
				{
					"client_id": "asd"
				},
				{
					"client_id": 7999
				},
				{
					"client_id": 7999,
					"public_key": "i am a public key"
				},
				{
					"client_id": 7999,
					"public_key": (1, 2, 3, 4, 5, 6)
				},
				{
					"client_id": 7999,
					"public_key": (1, 2, 3, 4, 5, 6, 7, 8)
				},
				{
					"client_id": 7999
				},
				{
					"client_id": 7999,
					"public_key": (4, 8, 7, 6, 3, 2, 1, 5)
				},
				{
					"client_id": 7999
				},
			]
		)

	def test(self, bodies: list[dict[str, any]]):
		for body in bodies:
			self.sendto(dumps(body).encode("ascii"), ("localhost", 8000))
			print("Sent:", body)
			data = self.recv(10240)
			print("Received:", loads(data))


if __name__ == '__main__':
	TestClient()
