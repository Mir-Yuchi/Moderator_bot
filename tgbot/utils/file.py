from pathlib import Path

from Levenshtein import ratio


def detect_obvious_word(obscene_words_file_path: str | Path,
                        phrase: str) -> bool:
    with open(obscene_words_file_path, encoding='utf-8') as file:
        for word in file:
            for part in range(len(phrase)):
                fragment = phrase[part: part + len(word)]
                distance = ratio(fragment, word)
                if distance >= .75:
                    return True
    return False
