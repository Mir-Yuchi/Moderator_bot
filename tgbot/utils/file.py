from pathlib import Path

from Levenshtein import ratio


def levenstein_range(phrase: str, word: str, percent: float = .40):
    for part in range(len(phrase)):
        fragment = phrase[part: part + len(word)]
        distance = ratio(fragment, word)
        if distance >= percent:
            return True


def detect_obvious_word(obscene_words_file_path: str | Path,
                        phrase: str, percent: float = .40) -> bool:
    with open(obscene_words_file_path, encoding='utf-8') as file:
        for word in file:
            if len(word) <= 4:
                percent = .40
            if levenstein_range(phrase, word, percent):
                return True
    return False


def detect_obv_list_word(word_list: list[str], text: str,
                         percent: float = .4) -> bool:
    for word in word_list:
        for part in range(len(text)):
            fragment = text[part: part + len(word)]
            distance = ratio(fragment, word)
            if distance >= percent:
                return True
    return False
