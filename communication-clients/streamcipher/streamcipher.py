from typing import Callable
from assign1.utils import byte_to_bits, bits_to_byte
from assign2.utils.config import WINDOW_SIZE


class StreamCipher(object):
	def __init__(self, generator: Callable[[any, int], str], key: any):
		self.generated_key = generator(key, WINDOW_SIZE)

	def crypt(self, body: dict[str, any]) -> dict[str, any]:
		low = body["offset"]
		high = low + len(body["text"]) if low + len(body["text"]) < WINDOW_SIZE else WINDOW_SIZE
		body["text"] = "".join([chr(bits_to_byte([bit1 ^ bit2 for bit1, bit2 in list(zip(x, y))])) for x, y in [(byte_to_bits(ord(byte1)), byte_to_bits(ord(byte2))) for byte1, byte2 in list(zip(body["text"], self.generated_key[low:high]))]])
		return body
