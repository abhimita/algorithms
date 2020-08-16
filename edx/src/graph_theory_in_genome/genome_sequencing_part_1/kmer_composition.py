import sys

def kmer_composition(k, text):
    """Computes the k-mer composition of string text

    Args:
        k:          integer length of k-mers to be found
        text:       string to split into a k-mer composition

    Returns:
        a string with each k-mer in text separated by newlines
    """
    return '\n'.join([text[i : i + k] for i in range(len(text) - k + 1)])


if __name__ == "__main__":
    k = int(sys.stdin.readline().strip())
    text = sys.stdin.readline().strip()

    print(kmer_composition(k, text))
