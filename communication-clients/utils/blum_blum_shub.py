def blum_blum_shub(seed: int, length: int) -> str:
	p = 30000000091
	q = 40000000003
	M = p * q

	key = []

	x = seed
	for _ in range(length):
		byte = 0
		for steps in range(8):
			x = x**2 % M
			byte += x % 2
			if int(steps) != 7:
				byte = byte << 1
		key.append(chr(byte))

	return "".join(key)
