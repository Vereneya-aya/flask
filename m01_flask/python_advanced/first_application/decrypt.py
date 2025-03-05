import sys


def decrypt(message: str) -> str:
    """
    Decrypts the given encoded message according to the given rules.
    """
    result = []
    i = 0
    while i < len(message):
        if message[i] == '.':
            if i + 1 < len(message) and message[i + 1] == '.':
                if result:
                    result.pop()
                i += 1  # Skip the next dot as well
            # Otherwise, just skip the single dot
        else:
            result.append(message[i])
        i += 1

    return ''.join(result)


if __name__ == "__main__":
    input_text = sys.stdin.read().strip()
    print(decrypt(input_text))
# echo "абраа..-.кадабра" | python3 decrypt.py