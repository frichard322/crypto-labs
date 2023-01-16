from assign2.streamcipher import StreamCipher
from utils.config import KEY, SEED, GEN_TYPE
from utils.solitaire import solitaire
from utils.blum_blum_shub import blum_blum_shub


def main() -> None:
	if GEN_TYPE == "solitaire":
		stream_cipher = StreamCipher(solitaire, key=KEY)
	elif GEN_TYPE == "blum-blum-shub":
		stream_cipher = StreamCipher(blum_blum_shub, key=SEED)
	else:
		print("ERROR: Wrong key generator type!")
		return

	text = "Contrary to popular belief, Lorem Ipsum is not simply random text."
	print(text)

	body: dict[str, any] = {
		"offset": 0,
		"text": text,
	}

	encrypted = stream_cipher.crypt(body)
	print(encrypted["text"])

	# If we modify the offset in-between the encryption and decryption we are going to lose the data.
	# encrypted["offset"] = 1

	decrypted = stream_cipher.crypt(encrypted)
	print(decrypted["text"])


if __name__ == "__main__":
	main()
