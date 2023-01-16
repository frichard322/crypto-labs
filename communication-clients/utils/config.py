# Type of key generator
GEN_TYPE: str = "solitaire"

# Key for solitaire generated with the following code:
# import random
# a = [chr(i) for i in range(50, 78)]
# random.shuffle(a)
# print("".join(a))

# Key for solitaire
KEY: str = "DM;C>IT?KN<=PHS@FU:JRELQOAGB"

# Seed for blum-blum-shub
SEED: int = 12345

# Higher number than 64 will make solitaire really slow
WINDOW_SIZE = 64
