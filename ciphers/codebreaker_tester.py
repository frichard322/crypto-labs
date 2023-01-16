from crypto import decrypt_vigenere_codebreaker


def main():
    dictionary = set()
    with open("words.txt", "r") as infile:
        for word in infile.readlines():
            dictionary.add(word.strip('\n'))

    with open("not_a_secret_message.txt", "r") as infile:
        message = infile.read().strip('\n')

    print(decrypt_vigenere_codebreaker(message, dictionary))


if __name__ == '__main__':
    main()
