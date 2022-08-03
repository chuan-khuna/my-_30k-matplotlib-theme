def generate_ngram(
    words: list[str], n: int, concatenate: bool = False
) -> list[tuple[str]]:
    if n <= 0:
        raise ValueError("n should be more than 1")

    if n > len(words):
        n = len(words)

    n_grams = []
    for current_index in range(0, len(words) - n + 1):
        n_gram_tuple = [
            words[current_index + n_gram_index] for n_gram_index in range(n)
        ]
        n_grams.append(tuple(n_gram_tuple))

    if concatenate:
        n_grams = ["".join(tuple_) for tuple_ in n_grams]
    return n_grams
