from assign2.client import Client


def main():
	client1 = Client(port=5555, name="Client1")
	client1.start_listening()
	client2 = Client(port=5556, name="Client2")
	client2.start_listening()

	client1.send_message(port=5556, body={"text": "YO, Can you read this? huehuehue"})
	client2.send_message(port=5555, body={"text": "Of course ;o"})
	client1.send_message(port=5556, body={"text": "That's bad..."})
	client2.send_message(port=5555, body={"text": "Why tho ?"})

	# Both process stops itself by sending a message to themselves
	client1.send_message(port=5555, body={"stop": 1})
	client2.send_message(port=5556, body={"stop": 1})


if __name__ == "__main__":
	main()
