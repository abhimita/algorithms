import sys


def reconstruct_string(patterns):
    """Reconstructs a string from its genome path

    Args:
        patterns:       a list of string k-mers in the order they appear in
                        text

    Returns:
        a string text with the given genome path
    """
    for i, p in enumerate(patterns):
        if i == 0:
            str = p
        else:
            str = str + p[-1:]
    return str


if __name__ == "__main__":
    patterns = sys.stdin.read().strip().splitlines()
    print(reconstruct_string(patterns))