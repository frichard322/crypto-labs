from string import ascii_letters, digits, punctuation
from random import choices

from merklehellman import mh

private = mh.generate_private_key()
public = mh.create_public_key(private)
i: int = 0


def test(msg: str):
    global i
    print(f"{i}.Test:")
    print("Message:", msg)
    e_msg = mh.encrypt_mh(msg, public)
    print("Encrypted:", e_msg)
    d_msg = mh.decrypt_mh(e_msg, private)
    print("Decrypted:", d_msg)
    i += 1
    if msg != d_msg:
        raise "Cypher failed: message != decrypted message"


def main():
    for _ in range(25):
        chars = ascii_letters + digits + punctuation
        msg = "".join(choices(chars, k=64))
        test(msg)


if __name__ == '__main__':
    main()
